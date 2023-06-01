#include <string>
#include <windows.h>

#pragma comment(linker, "/SUBSYSTEM:windows /ENTRY:mainCRTStartup")
// ^^^^ Disable console, recipe from: https://stackoverflow.com/a/6882500/636849
// WARN/limitations: * no stderr/stdout output
//                   * if the .exe process is killed, the node.exe child process will still live

void main(int argc, char *argv[] )
{
    STARTUPINFO si;
    PROCESS_INFORMATION pi;

    ZeroMemory( &si, sizeof(si) );
    si.cb = sizeof(si);
    //si.dwFlags = STARTF_USESHOWWINDOW;
    ZeroMemory( &pi, sizeof(pi) );

    // Build the command line, using absolute paths if possible:
    auto prog = std::string(argv[0]);
    auto pos = prog.find_last_of('\\');
    std::string command;
    if (pos == std::string::npos) {
        command = std::string("node.exe index.js");
    } else {
        auto path = prog.substr(0, pos);
        command = std::string(path);
        command.append("\\node.exe ");
        command.append(path);
        command.append("\\index.js");
    }
    // Append program arguments:
    for (int i = 1; i < argc; i++) {
        command.append(" ");
        command.append(argv[i]);
    }
    auto commandLPSTR = const_cast<char *>(command.c_str());
    //printf(commandLPSTR);printf("\n");

    // Start the child process:
    // (doc: https://learn.microsoft.com/fr-fr/windows/win32/procthread/creating-processes )
    if( !CreateProcess(
        NULL,                  // No module name (use command line)
        commandLPSTR,          // Command line
        NULL,                  // Process handle not inheritable
        NULL,                  // Thread handle not inheritable
        FALSE,                 // Set handle inheritance to FALSE
        CREATE_NO_WINDOW,      // No creation flags
        NULL,                  // Use parent's environment block
        NULL,                  // Use parent's starting directory 
        &si,                   // Pointer to STARTUPINFO structure
        &pi                    // Pointer to PROCESS_INFORMATION structure
    ) ) 
    {
        printf( "CreateProcess failed (%d).\n", GetLastError() );
        return;
    }

    // Wait until child process exits:
    WaitForSingleObject( pi.hProcess, INFINITE );

    // Close process and thread handles:
    CloseHandle( pi.hProcess );
    CloseHandle( pi.hThread );
}
