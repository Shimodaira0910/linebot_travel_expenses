from db_controller import DbController

class CommandActions:
    
    def __init__(self):
        self.__dbController = DbController()
    
    def witch_select_command(self, commands):
        if commands[0] == None or commands[0] == "":
            message = "そのコマンドはないんだぜ(涙)"
            return message
        elif commands[0] == "mem":
            self.select_add_command_action(commands)
            message = f"新しいメンバーを追加しました: 追加メンバー:{commands[1]}"
            return message
        else:
            message = "そのコマンドには対応してないヨ"
            return message
        # elif commands[0] == "al":
            
        # elif commands[0] == "red":
            
    def select_add_command_action(self, commands):
        username = commands[1]
        self.__dbController.insert_member_name(username)
        
    # def select_all_command_action():
        
        
    # def select_reduce_command_action():