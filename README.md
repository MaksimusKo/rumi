
# FastAPI Application Deployment with Apache and `screen`

This documentation provides step-by-step instructions to set up and run a FastAPI application using Apache as a reverse proxy and `screen` for session management. The process includes setting up a virtual environment, configuring Apache, and running the FastAPI application.

## Requirements

- Operating System: Ubuntu/Debian or CentOS/RHEL.
- Installed Apache HTTP Server.
- Installed Python and FastAPI.
- Installed Uvicorn (ASGI server for FastAPI).
- Installed `screen` for terminal session management.
- Domain name with an SSL certificate (optional, for HTTPS).

## Steps for Setup

### 0. Setting up VM (google cloud, AWS)
Clone this repo, or any other repo

sudo git clone (repo link)

install cuda drivers (depends on OS)

https://developer.nvidia.com/cuda-downloads
Or do it using github repo.

sudo apt update
sudo apt upgrade
sudo apt install build-essential dkms

sudo apt remove --purge '^nvidia-.*'

git clone https://github.com/NVIDIA/cuda-install-scripts.git
cd cuda-install-scripts
sudo ./install_cuda.sh

### 1. Creating and Using a `screen` Session
Install screen.
sudo apt install screen 

Create a new `screen` session to isolate your process:

```bash
screen -S rumi_session
```

If you need to use `sudo`:

```bash
sudo screen -S rumi_session
```

### 2. Navigating to the Project Directory

Change to the directory where your FastAPI project is located:

```bash
cd /path/to/rumi
```

### 3. Activating the Virtual Environment

Activate the Python virtual environment to isolate project dependencies:

```bash
source venv/bin/activate
```

### 4. Enabling and Starting Apache

Ensure that Apache is configured to start automatically on system boot and start it:

Enable Apache to start on boot:

```bash
sudo systemctl enable apache2
```

Start Apache:

```bash
sudo systemctl start apache2
```

### 5. Checking Apache Status

Verify that Apache is running:

```bash
sudo systemctl status apache2
```

You should see a message indicating that Apache is active and running.

### 6. Launching the FastAPI Application

Start your FastAPI application using Uvicorn:

```bash
uvicorn myapp:app --host 0.0.0.0 --port 8000
```

Make sure that `myapp:app` matches the path to your FastAPI application in the format `module:app`.

### 7. Managing Screens

`screen` allows you to switch between virtual terminals.

To detach from the current `screen` session and leave it running in the background, press:

```bash
Ctrl + A + D
```

To reattach to a previously created `screen` session:

```bash
screen -r rumi_session
```

Or, if you have multiple sessions, list all active `screen` sessions and reattach to the desired one:

```bash
screen -ls
screen -r <ID>
```

Replace `<ID>` with your session's identifier.

### 8. Verifying Apache Configuration

Ensure that the Apache configuration for your site is correct.

Open the Apache configuration file for your site:

```bash
sudo nano /etc/apache2/sites-available/rumi.conf
```

Ensure the configuration includes correct settings for proxying requests to your FastAPI application. Example configuration:

```apache
<VirtualHost *:443>
    ServerName your_domain.com
    DocumentRoot /var/www/html

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/your_domain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/your_domain.com/privkey.pem

    # Proxy settings
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/

    <Proxy *>
        Require all granted
    </Proxy>

    <Directory /var/www/html>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

**Ensure that the `proxy` and `proxy_http` modules are enabled:**

```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
```

Restart Apache after making changes:

```bash
sudo systemctl restart apache2
```

### Additional Recommendations

- **Security**: Ensure files and directories have correct permissions and ownership to prevent unauthorized access.
- **Logs**: Regularly check Apache and application logs for errors and issues.
- **Automation**: Consider using process management tools like `supervisor` or `systemd` to manage your FastAPI application.

These steps will help you successfully run a FastAPI application using Apache and `screen`. If you encounter any issues or have additional questions, feel free to ask!
