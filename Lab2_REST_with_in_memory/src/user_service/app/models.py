class UserEntity:
    
    NEXTID = 0
    
    def __init__(self, id: int, nick: str, fname: str, lname: str, password_hash: str):
        self.id = UserEntity.NEXTID
        UserEntity.NEXTID += 1
        self.nick = nick
        self.fname = fname
        self.lname = lname
        self.password_hash = password_hash
        
    def __repr__(self):
        return f'User-{self.id}({self.fname} {self.lname} {self.nick} {self.password_hash})'