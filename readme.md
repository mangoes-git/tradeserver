# Readme

## Connecting to ssh

1. Find the server's ip address and your username and password.
    - The username should be `debian` by default on OVH's VPS.
2. Open your terminal application:

    - On Windows find the command prompt (type `CMD` in search) or the [Windows Terminal](https://apps.microsoft.com/detail/9n0dx20hk701?rtc=1&hl=en-ca&gl=CA).

    - On Mac open the Terminal app.

3. Inside the terminal, type `ssh <username>@<serverip>` (replacing your username and server ip) and press `enter`. For example `ssh debian@192.88.142.173`.
    - The command prompt may ask you whether you want to trust the connection, type `yes` and press `enter` to accept.
    - The command prompt will ask you for the password. Keep in mind that nothing will be shown in the terminal while you are typing it. Once you have typed your password press `enter` or `control + c` to cancel.
4. Once you are logged into the server, type `cd tradeserver` to get into the project's directory.
5. The following commands are available: - `make stop` to stop the server application. - `make start` to start it. - `make watch-logs` to stream the log output (live). Press `control + c` to exit.
   ![image]()
