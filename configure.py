#!/usr/bin/python3
with open("./env") as template:
    username = input("Enter the IB username: ")
    password = input("Enter the password for the account: ")
    trading_mode = input("Which trading mode to use?\n1. paper\n2. live\n")
    if trading_mode == "1":
        trading_mode = "paper"
    elif trading_mode == "2":
        trading_mode = "live"
    else:
        print("Invalid trading mode.")
        exit()
    print("Configuring server with the following values:")
    print(f"\tusername: {username}")
    print(f"\tpassword: {password}")
    print(f"\ttrading mode: {trading_mode}")
    verify = input("Is this correct? (y/N):")
    if verify.lower() != "y":
        print("Configuration cancelled.")
        exit()
    result = []
    for line in template:
        if line[0] == "#":
            continue
        parts = line.strip().split("=")
        key = parts[0]
        if key == "TWS_USERID":
            parts[1] = username
        if key == "TWS_PASSWORD":
            parts[1] = password
        if key == "TRADING_MODE":
            parts[1] = trading_mode
        result.append(parts)

text = "\n".join(["=".join(pair) for pair in result])

with open(".env", "w") as f:
    f.write(text)

print("Configuration complete.")
