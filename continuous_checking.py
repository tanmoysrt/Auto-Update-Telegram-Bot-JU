import time
import update_checker
import db_commands
import json
from deepdiff import DeepDiff
from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
command_to_send = 'start cmd /k "python send_messages_telegram.py -t {} -name_id {} -token {} && exit"'
frequency = 1800 # 60*30 -- 30 minutes



def main():
    while True:
        # Check Notice Sections And Update & Trigger messages
        step_f = 1
        step_s = 1
        for i in db_commands.getJuNoticeSectionsData():
            full_name = i[1]
            link = i[2]
            data = json.loads(i[3])
            name_id = i[4]
            print(f"CHECK NOTICE SECTION : {step_f}")
            try:
                counts,current_data = update_checker.getWholeData(link)
                if len(DeepDiff(current_data, data, ignore_order=True))==0:
                    print("Not Updated Notice Section")
                else:
                    db_commands.updateDataOfNoticeSection(current_data,name_id)
                    print("Updated Notice Section")
                    os.system(command_to_send.format("group",name_id,bot_token))
                    os.system(command_to_send.format("private",name_id,bot_token))
            except Exception as e:
                print(f"Failed in notice section checking : {e}")
            step_f+=1

        # Check If homepage updated or not and update hash in database
        try:
            print(f"CHECK HOMEPAGE : {step_s}")
            current_hash_homepage,updated =  update_checker.JUHomePageCheck()
            if updated:
                db_commands.updateCurrentHashOfJUHomePage(current_hash_homepage)
                print("Updated JU Homepage")
                os.system(command_to_send.format("group", "ju", bot_token))
                os.system(command_to_send.format("private", "ju", bot_token))
            else:
                print("Not updated JU Homepage")
        except Exception as e:
            print(f'Failed in homepage updation section : {e}')
        step_s += 1

        time.sleep(frequency)



if __name__ == '__main__':
    main()
