
# Dicoria (重瞳)

Dicoria is a tool used to identify Content Management Systems (CMS) based on the website's response. It utilizes various techniques and fingerprinting methods to determine the CMS being used.

Dicoria 是一款根据网站响应识别内容管理系统 (CMS) 的工具。它利用各种技术和指纹识别方法来确定网站正在使用的 CMS。

![图片](https://github.com/R4be1/Dicoria/assets/110738599/4e752202-3705-4145-b5b1-7e21fe1d097f)


## Installation

1. Clone this repository:
   ```
   git clone https://github.com/R4be1/Dicoria.git
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
   
## Usage

To use Dicoria, follow the steps below:

1. Open a terminal and navigate to the cloned repository's directory.

2. Execute the following command, replacing `<website>` with the target website URL:
   ```
   python3 Dicoria.py -u <website>
   ```

   Example:
   ```
   python3 Dicoria.py -u 'http://www.example.com'
   ```

3. The tool will start identifying the CMS used by the website. Progress will be displayed as it scans different URLs and analyzes responses.

4. After the scan completes, the identified CMS names will be shown in the terminal.

## Acknowledgements

![Dicoria was developed by Rebel.](https://github.com/R4be1/)

![Rebel's GitHub stats](https://github-readme-stats.vercel.app/api?username=R4be1&show_icons=true&theme=radical)

## Disclaimer

This tool is intended for educational purposes only. Use it responsibly and respect the privacy of others.
```
Please note that this `readme.md` assumes a certain folder structure and includes some instructions specific to the installation and usage of the tool. Modify it accordingly based on your project's requirements.
```
