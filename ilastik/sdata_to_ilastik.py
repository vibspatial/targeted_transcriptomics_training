from pathlib import Path
from typing import Any, Iterable, Tuple, Optional
from spatialdata import SpatialData
import h5py
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
import os
import harpy as hp
from harpy.table._table import add_table_layer
from harpy.utils._keys import _REGION_KEY

def _create_h5(images_dict, output_path):
    with h5py.File(output_path, 'w') as hf:
        for dataset_name, img_data in images_dict.items():
            hf.create_dataset(dataset_name, data=img_data, chunks=(512, 512))

def export_h5(
    sdata: SpatialData,
    img_layer: str = None, 
    labels_layer: str = None, 
    channels: str | Iterable[str] | None = None, 
    output: str | Path | None = None,
    crd: Optional[Tuple[int, int, int, int]] = None,
) -> None:
    """
    Exports an .h5 file from an image layer or labels layer for training in Ilastik.

    Args:
        sdata:
            The SpatialData object containing the images/masks to be exported.
        img_layer:
            Image layer to be exported.
        labels_layer:
            Labels layer to be exported.
        channels:
            Channels in an image layer that will be exported. If None, all channels will be exported.
        output:
            Output path of .h5 file to be exported.
        crd:
            The coordinates for the region of interest in the format (xmin, xmax, ymin, ymax). If None, the entire image is exported.
    Returns:
    -------
    None
    """

    if img_layer is not None and labels_layer is not None:
        raise ValueError(
            "Both img_layer and labels_layer is not None. Please specify either img_layer or labels_layer, not both."
        )       

    if channels is not None:
        channels = list(channels) if isinstance(channels, Iterable) and not isinstance(channels, str) else [channels]
        if labels_layer is not None:
            raise ValueError(
                "Both labels_layer and channels is not None. Please do not specify channels when using labels_layer."
            )  
    elif channels is None:
        if img_layer is not None:
            channels = [channel.item() 
                for channel in hp.im._image._get_spatial_element(sdata, img_layer).c]
            
            print(
                f"No channel names specified. "
                f"Default to exporting all channels in image layer {img_layer}."
            )
        
    if img_layer is not None:
        images_dict = {}
        for i, channel in enumerate(hp.im._image._get_spatial_element(sdata, img_layer).c.data):
            if channel not in channels:
                raise ValueError(f"{channel} is not in the specified list of channels.")
            else:
                image_data = hp.im._image._get_spatial_element(sdata, img_layer)[i].compute().data
                if crd:
                    xmin, xmax, ymin, ymax = crd
                    image_data = image_data[ymin:ymax, xmin:xmax]
                images_dict[f'{channel}'] = image_data
    elif labels_layer is not None:
        label_data = hp.im._image._get_spatial_element(sdata, labels_layer).compute().data
        if crd:
            xmin, xmax, ymin, ymax = crd
            label_data = label_data[ymin:ymax, xmin:xmax]
        if label_data.dtype == 'int32':
            label_data = label_data.astype('uint32')
        images_dict = {labels_layer: label_data}
    else: 
        raise ValueError(
            "No image layer or labels layer specified. " "Please specify either img_layer or labels_layer"
        )
        
    _create_h5(
    images_dict=images_dict, 
    output_path=output
)
    
def _read_and_preprocess_ilastik_( 
    input_path: str | Path,
):
    # Read and filter ilastik table
    if input_path.endswith('h5'):
        with h5py.File(input_path, "r") as data:
            dataset = data["table"][:]
            ilastik_df = pd.DataFrame({col: dataset[col].astype(str) if dataset[col].dtype.kind == 'S' else dataset[col] for col in dataset.dtype.names})
    elif input_path.endswith('csv'):
            ilastik_df = pd.read_csv(input_path)
    
    # Renaming columns
    ilastik_df.rename(columns={
        'User Label': 'ilastik_user_label',
        'Predicted Class': 'ilastik_predicted_class',
        'Center of the object_0': 'ilastik_centroid_x',
        'Center of the object_1': 'ilastik_centroid_y'
    }, inplace=True)

    # Renaming probability columns
    probability_columns = [col for col in ilastik_df.columns if col.startswith('Probability of')]
    for col in probability_columns:
        new_col_name = f'ilastik_probability_{col.split(" ")[-1]}'
        ilastik_df.rename(columns={col: new_col_name}, inplace=True)

    # Selecting the columns to keep
    columns_to_keep = [
        'ilastik_user_label',
        'ilastik_predicted_class',
        'ilastik_centroid_x',
        'ilastik_centroid_y'
    ] + [col for col in ilastik_df.columns if col.startswith('ilastik_probability_')]

    ilastik_df = ilastik_df[columns_to_keep]
    
    # Rename cells without user labels
    class_names = ilastik_df['ilastik_predicted_class'].unique()
    
    for index, row in ilastik_df.iterrows():
        ilastik_user_label = row['ilastik_user_label']
        if ilastik_user_label not in class_names:
            ilastik_df.at[index, 'ilastik_user_label'] = 'no_user_label'
    
    return ilastik_df

def _return_ilastik_data_for_nearest_cell(
    row, 
    ilastik_df,
    centroid_column_x,
    centroid_column_y):
    # Extract coordinates
    adata_coordinates = (row[centroid_column_x], row[centroid_column_y])
    ilastik_coordinates = ilastik_df[['ilastik_centroid_x', 'ilastik_centroid_y']]

    # Calculate distances
    distances = cdist([adata_coordinates], ilastik_coordinates)[0]

    # Find nearest neighbor
    nearest_neighbor_index = np.argmin(distances)
    nearest_neighbor = ilastik_df.iloc[nearest_neighbor_index]

    return nearest_neighbor

def add_ilastik_to_sdata(
    sdata: SpatialData,
    input_path: str | Path = None,
    table_layer: str | None = None, 
    labels_layer: str = None, 
    centroid_column_x: str = None,
    centroid_column_y: str = None, 
    suffix: str = None):
    """
    Adds the ilastik predicted classes, the ilastik probabilities for each class and the user labels to each cell in a SpatialData table. 
    Since the object identities are not preserved in ilastik, it is necessary to supply the centroid coordinates so that each cell can be matched to the closest corresponding ilastik object.

    Args:
        sdata:
            The SpatialData object containing the table to which the ilastik results will be added.
        input_path: 
            The path to the .h5 or .csv output files from the Ilastik object classifier.
        table_layer:
            The table layer in `sdata.tables` to which the ilastik results will be added.
        labels_layer:
            The label layer that corresponds to the data in the table layer.
        centroid_column_x: 
            The name of the column containing each cell's centroid x-coordinate in the obs layer of the SpatialData table.
        centroid_column_y: 
            The name of the column containing each cell's centroid y-coordinate in the obs layer of the SpatialData table.
        suffix: 
            A tag that can be added to each ilastik column to clarify which ilastik object classifier they come from.
        
    Returns:
    -------
    SpatialData
        The input SpatialData object updated with the ilastik predictions, probabilities and user labels added as columns in the table's obs layer.
    """
    
    if table_layer is None:
        raise ValueError("Please specify a `table_layer`")
    
    if labels_layer is None:
        raise ValueError("Please specify a `labels_layer`")
    
    if centroid_column_x is None or centroid_column_y is None:
        raise ValueError("Please specify the names of the columns containing the centroid coordinates using centroid_column_x and centroid_column_y")
    
    # Read and preprocess ilastik results
    ilastik_df = _read_and_preprocess_ilastik_(input_path)
    
    # Match ilastik objects to sdata objects
    merged_data = sdata.tables[table_layer].obs.apply(
        _return_ilastik_data_for_nearest_cell,
        axis = 1, 
        ilastik_df = ilastik_df,
        centroid_column_x = centroid_column_x,
        centroid_column_y = centroid_column_y)
    
    merged_data = merged_data.drop(columns=['ilastik_centroid_x', 'ilastik_centroid_y'])
    
    # Add suffix
    if suffix is not None:
        merged_data.columns = [col + '_' + suffix for col in merged_data.columns]

    # Add ilastik data to sdata table layer
    adata = sdata.tables[table_layer].copy()
    for col in merged_data.columns:
        adata.obs[col] = merged_data[col]
        
    # Add table layer to back to zarr
    sdata = add_table_layer(
        sdata,
        adata=adata,
        output_layer=table_layer,
        region=labels_layer,
        overwrite=True,
    )
    
    return sdata
    
    
def assign_ilastik_cell_types(
    sdata, 
    table_layer: str | None = None, 
    labels_layer: str = None, 
    annotation_table_path: str = None, 
    output_column: str = 'ilastik_cell_types', 
    default_value: str = 'other'):
    """
    Assigns cell types based on a provided annotation table that contains cell types and the corresponding conditions. 
    Row names in the annotation table should correspond to the names of the ilastik object classifiers, while columns should refer to the desired cell type names. 
    Values in the table should correspond to class names from the appropriate object classifiers or should be empty (in which case they will be ignored).

    Args:
        sdata:
            The SpatialData object containing columns in sdata.table.obs with predictions from ilastik object classifiers.
        table_layer:
            The table layer in `sdata.tables` to which the cell types will be added.
        labels_layer:
            The label layer that corresponds to the data in the table layer.
        annotation_table_path:
            Path to the annotation table (as a csv file) containing the rules to assign cell types.
        output_column:
            Name of the new column containing the provided cell types. Defaults to 'ilastik_cell_types'.
        default_value:
            Values used for all cells that do not fit any of the conditions. Defaults to 'other'.

    Returns:
    -------
    SpatialData
        The input SpatialData object updated with a new column in the table's obs layer where cell types have been assigned.
    """
    if table_layer is None:
        raise ValueError("Please specify a `table_layer`")
    
    if labels_layer is None:
        raise ValueError("Please specify a `labels_layer`")
    
    annotation_table = pd.read_csv(annotation_table_path, index_col=0)
    
    adata = sdata.tables[table_layer].copy()

    adata.obs[output_column] = default_value

    for column in annotation_table.columns:
        for row in annotation_table.index:
            if f'ilastik_predicted_class_{row}' not in adata.obs.columns:
                raise ValueError(f"Column '{f'ilastik_predicted_class_{row}'}' does not exist in table. Please check the row names in the provided annotation table carefully.")

            annotation_value = annotation_table.loc[row, column]
            if not pd.isnull(annotation_value) and annotation_value not in adata.obs[f'ilastik_predicted_class_{row}'].unique():
                raise ValueError(f"Value '{annotation_value}' for cell type '{column}' does not exist in the corresponding '{f'ilastik_predicted_class_{row}'}' column in the table. Please check the ilastik class names in the provided annotation table carefully.")

        conditions = [adata.obs[f'ilastik_predicted_class_{row}'] == annotation_table.loc[row, column] for row in annotation_table.index if not pd.isnull(annotation_table.loc[row, column])]
        
        condition = conditions[0]
        for cond in conditions[1:]:
            condition &= cond
            
        if (adata.obs.loc[condition, output_column] != default_value).any():
            raise ValueError(f"Assigning cell type '{column}' results in a conflict in the '{output_column}' column and will overwrite a previously assigned cell type. Please check the conditions in the provided annotation table carefully.")

        adata.obs.loc[condition, output_column] = column
        
    # Add table layer to back to zarr
    sdata = add_table_layer(
        sdata,
        adata=adata,
        output_layer=table_layer,
        region=labels_layer,
        overwrite=True,
    )
        
    return sdata


def combine_ilastik_predictions(
    sdata,
    table_layer: str | None = None, 
    labels_layer: str = None, 
    output_column: str = 'ilastik_combination', 
    ilastik_columns_to_combine: list = None):
    """
    Combines predictions from different ilastik columns into a single column.

    Args:
        sdata: SpatialData
            The SpatialData object containing columns in sdata.table.obs with predictions from ilastik object classifiers.
        table_layer:
            The table layer in `sdata.tables` to which the cell types will be added.
            The label layer that corresponds to the data in the table layer.
        output_column: str, optional
            Name of the new combined column. Defaults to 'ilastik_combination'.
        ilastik_columns_to_combine: list of str, optional
            List of the columns containing ilastik predictions that need to be combined.
            If not provided, all columns containing ilastik predictions will be combined.

    Returns:
    -------
    SpatialData
        The input SpatialData object updated with a new column in the 'sdata.table.obs' that contains the combination of all input columns.
    """
    
    if table_layer is None:
        raise ValueError("Please specify a `table_layer`")
    
    if labels_layer is None:
        raise ValueError("Please specify a `labels_layer`")
    
    if ilastik_columns_to_combine is None:
        print("List of ilastik columns to combine is not provided. Will default to combining all ilastik prediction columns.")
        ilastik_columns_to_combine = [col for col in sdata.table.obs.columns if col.startswith('ilastik_predicted_class_')]    
    
    adata = sdata.tables[table_layer].copy()
    
    adata.obs[output_column] = ""
    
    for column in ilastik_columns_to_combine:
        if column not in adata.obs:
            raise ValueError(f"Column '{column}' not found in the adata.")
        adata.obs[output_column] += adata.obs[column].astype(str) + "-"
    
    adata.obs[output_column] = adata.obs[output_column].str.rstrip("-")
    
    # Add table layer to back to zarr
    sdata = add_table_layer(
        sdata,
        adata=adata,
        output_layer=table_layer,
        region=labels_layer,
        overwrite=True,
    )
    
    return sdata 