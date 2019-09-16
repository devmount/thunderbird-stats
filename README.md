# Thunderbird Email Stats

[![release](https://img.shields.io/badge/release-v0.1.2-30cef2.svg?style=flat-square)](https://github.com/devmount/thunderbird-stats/releases) [![license](https://img.shields.io/badge/license-MIT-30cef2.svg?style=flat-square)](./LICENSE) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-30cef2.svg?style=flat-square)](./CONTRIBUTING.md)


Generate simple but awesome analytics of your Thunderbird mail account

![thunderbird_email_stats](https://user-images.githubusercontent.com/5441654/64927404-d1a47780-d80a-11e9-899e-c4b55f8e2bbe.jpg)

## Get started

This toolkit uses Python to retrieve the data from your Thunderbird mail account and store it in `json` format and a Vue.js based web application to present the data in numbers and charts.

### Installation

Make sure, you have at least Python 3.6 installed with the `tqdm` package

```bash
$ python --version
Python 3.6.9
$ pip install tqdm
...
```

Clone this repository and enter its root directory:

```bash
git clone https://github.com/devmount/thunderbird-stats
cd thunderbird-stats
```

Install all dependencies:

```bash
yarn
```

Make the Python script executable:

```bash
chmod +x ./stats.py
```

### Configuration

Before using this tool, you have to set two settings in the `config.ini`: The file path to your Thunderbird profile and your own email address(es) for the Python script to recognize, which emails were sent or received. You can determine your profile file path by right-clicking on your Thunderbird account > Settings > Server-Settings > Scroll to the bottom. Your email addresses are comma seperated without spaces. See this example:

```ini
[email]
ThunderbirdProfilePath = /path/to/Thunderbird/Profiles/abcdefg.default/ImapMail/server
EmailAddresses = your@email.com,test@email.com
```

> **IMPORTANT**  
> Your Thunderbird account **must** be configured as `maildir`, where each message is stored as a seperate file. Otherwise, this tool won't work.

### Usage

Now that everything is set, you can run the Python script. A progress indicator will show you, how many emails are processed and how long it will take to finish. This could be a possible output:

```bash
$ ./stats.py
Processing mails...
100%|██████████████████████████████| 24654/24654 [00:27<00:00, 907.48mails/s]
Finished.
```

Once finished, all data files are created in the `/src/data` directory in `json` format. Now you can either start the development server and find your stats at `localhost:8080`...

```bash
yarn serve
```

... or create an optimized production build with minification. All build files can be found in the `dist` directory and you can open the `index.html` file to find your stats.

```bash
yarn build
```

## Additional notes

- Keep in mind, that the processing of large mailboxes can take a lot of time.
- Unfortunately there is no unified email date format, so it's very likely that the Python script will not recognize all of your emails

## Licence

[MIT License](./LICENSE)

---

This tool is completely free to use. If you enjoy it, please consider [donating via Paypal](https://paypal.me/devmount) for further development. :green_heart:
