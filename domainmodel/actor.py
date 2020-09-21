
class Actor:
    def __init__(self, actor_full_name:str ):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
            self.__actor_colleague = list()
        else:
            self.__actor_full_name = actor_full_name.strip()
            self.__actor_colleague = list()
    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    @property
    def actor_colleague(self):
        return self.__actor_colleague

    def add_actor_colleague(self, colleague):
        if isinstance(colleague, Actor):
            self.actor_colleague.append(colleague)
            colleague.actor_colleague.append(self)

    def check_if_this_actor_worked_with(self, colleague):
        return colleague in self.actor_colleague

    def __repr__(self):
        return "<Actor {}>".format(self.actor_full_name)
    
    def __eq__(self, other):
        if not isinstance(other, Actor):
            return False
        if self.actor_full_name is None and other.actor_full_name is None:
            return False
        return self.actor_full_name == other.actor_full_name

    def __lt__(self, other):
        return self.actor_full_name < other.actor_full_name

    def __hash__(self):
        return hash(self.actor_full_name)



