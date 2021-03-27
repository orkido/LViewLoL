# Fork Details
!!! IMPORTANT !!! This uses VS2019 and the mvc142 toolkit, please be sure your environment matches this configuration before attempting to build, and ofcourse you will still need to follow the steps outlined for the original project. Orkido on UC has documented much of what you need to do in order to get the project building from VS2019 so if you have trouble please search the LView thread for his comments on the matter.

Note:  In some few cases depending on your Windows installation or whether you had Python installed beforehand your Python might not have properly set the system environment variables. If you run into the case where you are able to successfully compile the app but it instantly closes after running it (be sure to have followed the steps properly), then you may need to set the Python path in your environment variables manually; to be safe, add the path to the User's 'Path', System's 'Path' variables, and then add a PYTHONHOME variable if you don't have it and point it to your root Python directory.

# LViewLoL
!!! IMPORTANT !!! I've noticed riot already has taken notice of this project and they have implemented a few signatures for detecting this. Don't use this as it is, if you know what you are doing you will have a clue what to modify to avoid detection. Also careful if you want to copy paste code from here to an internal it seems riot has taken an extra step in making some code signatures.

### What is this
LView is a python based scripting platform for League of Legends. The engine is external that means it is not injected into leagues process. The engine is running in a separate process and reads the games state using ReadProcessMemory.

Key features of LView:
  1. Ability to create overlays and automatize gameplay using python scripts
  2. Performant ingame overlays/menus using a combination of directx, direct composition and dear imgui 
  3. Static game data available at runtime. Data is unpacked directly from the game files. Taken from https://www.communitydragon.org/ .
  4. Undetectability. Since LView reads the game state externally the ban probability is close to 0. Currently since the start of the development there is no recorded case of a ban.
  5. A rich set of premade scripts. There are a lot of already implemented and tested gameplay scripts by default in LView and more are to come. Some of these scripts: orbwalker, spell tracker, champion tracker, map awareness, minimap drawings, skillshot drawings... etc 
 
![Screenshot](https://i.imgur.com/IK9SxKd.png)

### Building

You need Visual Studio 2019 to compile this.
Dependencies:
  1. python39: dlls and includes are already in project. You need to install python 3.9 for 32bits (Make sure you check the Add to PATH checkbox in the installer: https://www.python.org/ftp/python/3.9.0/python-3.9.0.exe)
  3. aws-lambda: dlls and includes are already in project (was used for authentication)
  3. directx 11: Must install directx end user runtimes: https://www.microsoft.com/en-us/download/details.aspx?id=35 .Extract this and run dxsetup
  4. boost::python. Due to the size of the boost libraries you must download boost yourself:
      1. Download boost 1.75.0 (https://www.boost.org/users/history/version_1_75_0.html)
      2. Unarchive it in LView/boost
  5. Compile the app on Release x86 (you need to compile boost::python on debug to compile on debug, which I didn't).
  6. Copy Release/ConsoleApplication.exe to LView/ConsoleApplication.exe overwriting the existing file if needed
  7. Run LView/ConsoleApplication.exe and have fun!
 ### Setup
 All LView & LView python scripts configurations reside in config.ini file. First you must set the path to the scripts folder with the following config (you can find the config.ini in LView folder):
 
  `::scriptsFolder=\<folder\>`
