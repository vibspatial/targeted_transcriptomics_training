import javafx.application.Platform
import qupath.lib.gui.commands.ProjectImportImagesCommand
import qupath.lib.images.ImageData
import qupath.lib.images.servers.ConcatChannelsImageServer
import qupath.lib.images.servers.ImageServerProvider

import java.awt.image.BufferedImage
import static qupath.lib.gui.scripting.QPEx.*

def folderPath = 'D:/example_data_MACSima/REAscreen_IO_CRC/REAscreen_IO_CRC'  // <-- Update this to your folder
def folder = new File(folderPath)

if (!folder.isDirectory()) {
    print 'Invalid folder path'
    return
}

// Filter supported image files (you can customize extensions)
def imageFiles = folder.listFiles({ file -> 
    file.isFile() && file.name.toLowerCase().matches('.*\\.(tif|tiff|jpg|jpeg|png)$') 
} as FileFilter)

if (imageFiles == null || imageFiles.length == 0) {
    print 'No image files found in folder.'
    return
}

// Sort for consistent channel order, optional
imageFiles = imageFiles.sort { it.name }

// Build servers for each channel
def channelServers = imageFiles.collect {
    ImageServerProvider.buildServer(it.absolutePath, BufferedImage)
}

// Create a concatenated server
def server = new ConcatChannelsImageServer(channelServers[0], channelServers)
def imageData = new ImageData(server)

Platform.runLater {
    def project = getProject()
    ProjectImportImagesCommand.addSingleImageToProject(project, server, null)
    project.syncChanges()
    getQuPath().refreshProject()
}