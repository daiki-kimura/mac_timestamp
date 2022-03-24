Timestamp for Wake and Sleep on Mac 
===
１日の初回起動と最終スリープ時刻の自動記録スクリプト．各自の勤怠管理の参考程度にご活用下さい．

- Script automatically saves these information
  - First wake-up time from sleep for each day
  - Last sleep time for each day
  - Output format: `date, first wake-up time, last sleep time`

  - Example: 
  
    `2018-03.txt`
    ```text
    2018-03-01, 09:00:13, 18:54:02
    2018-03-02, 09:15:35, 19:16:10
    ```
    
- This is for "Sleep" on Mac (not "Shutdown" or "Reboot")

## Setup

### 1. Clone repository or Download python file

```bash
cd (install_folder_path)
git clone https://github.com/daiki-kimura/mac_timestamp.git
```

### 2. Change folder path

Set folder path in `timestamp.py` by your-self 

```text
TIMESTAMP_FOLDER: folder path for timestamp files (must be changed)
BORDER_TIME_FOR_DAYS: your border time for days (default: '03:00:00')
```

### 3. Set schedule

Set by Crontab

```bash
crontab -e
```

- add these text

  ```text
  * */3 * * * python (install_folder_path)/timestamp.py >/dev/null 2>&1
  # Of course, you can change frequency yourself
  # Example: * */3 * * * python3 /Users/daiki/.dotfiles/mac_timestamp/timestamp.py >/dev/null 2>&1
  ```

## Environment

Tested on 

- Mac OS 12.3
- Python 3.7.9

## Special thanks

- pmset command: https://apple.stackexchange.com/questions/52064/how-to-find-out-the-start-time-of-last-sleep
- inspired by https://qiita.com/hidesakai/items/da7fca1919ed7e32975c
