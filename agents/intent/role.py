from metagpt.roles.role import Role, RoleReactMode
from metagpt.schema import Message
from .action import RecvAndAnalyze
from dotenv import load_dotenv

load_dotenv()

class IntentReg(Role):
    name: str = "IntentReg"
    profile: str = "intent recognition"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_actions([RecvAndAnalyze])
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)

    async def _act(self) -> Message:
        todo = self.rc.todo

        msg = self.get_memories(k=1)[0]
        result = await todo.run(instruction=msg.content)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        return msg
