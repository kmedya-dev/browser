# How to Fix Build Errors

Any error that shows up in the CI/CD build process is almost certainly fixable. This is a critical point, and it's why we set up the CI/CD pipeline the way we did.

### Why the Errors Are Fixable

1.  **You have an AI assistant:** My primary role is to help you with this. If an error occurs, you can paste the log file contents, and I can analyze them to identify the exact cause and provide the precise steps to fix it. I have been trained on a vast number of build logs and can recognize common (and uncommon) failure patterns.

2.  **The logs are detailed:** The `buildozer.log` file is extremely verbose. It tells us exactly what command failed and why. It's not a mystery box; it's a detailed report. We just need to read it.

3.  **The fixes are usually simple:** 99% of build errors are solved by making small, specific changes to your configuration files.

### The Most Common (and Fixable) Errors

Here are the most likely problems you might see and how they are fixed:

| Error Type             | What it looks like in the log                  | How We Fix It                                                                                                                               |
| ---------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Recipe Failure**     | `ERROR: Recipe build failed: pyjnius`          | This is the most common issue. We fix it by changing a version number in `buildozer.spec` or `requirements.txt`. (e.g., `pyjnius==1.5.0`). |
| **Missing Dependency** | `Command failed: pip install ... some-package` | We add the missing package name to the `requirements` line in `buildozer.spec`.                                                           |
| **NDK/SDK Version**    | `Compiler failed... check NDK version`         | We change the NDK version in `buildozer.spec` (e.g., from `android.ndk = 25b` to `android.ndk = 26c`).                                     |
| **Typo in `spec` file**| `Buildozer failed to parse spec file`          | We find and correct the typo in `buildozer.spec`.                                                                                           |

As you can see, the solution is almost always a one-line change in a text file.

### The Simple Plan for Fixing Any Error

You are not on your own. We have a clear, simple process:

1.  You push the code to GitHub.
2.  The build runs. If it fails, you download the `buildozer-log` artifact from the "Actions" tab.
3.  **You share the log with me.**
4.  **I will tell you exactly what to change.**
