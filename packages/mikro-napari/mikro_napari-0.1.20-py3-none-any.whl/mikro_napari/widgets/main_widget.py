from arkitekt.schema.widgets import SearchWidget
from mikro_napari.helpers.stage import StageHelper
from arkitekt.messages.postman.provide.bounced_provide import BouncedProvideMessage
from qtpy import QtWidgets
from herre import HerreClient
from arkitekt.agents.qt import QtAgent
from mikro.widgets import MY_TOP_REPRESENTATIONS
from mikro.schema import Representation, Sample

class ArkitektWidget(QtWidgets.QWidget):

    def __init__(self, napari_viewer, *args, bergen_params = {}, config_path="napari.yaml", **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.loginButton = QtWidgets.QPushButton("Login!")
        self.loginButton.clicked.connect(self.login)
        self.layout.addWidget(self.loginButton)

        self.app = QtWidgets.QApplication.instance()
        self.app.lastWindowClosed.connect(self.close)

        self.status = QtWidgets.QLabel("Arnheim")
        self.helper = StageHelper(napari_viewer)

        self.provisionsWidget = QtWidgets.QListWidget()
        self.layout.addWidget(self.provisionsWidget)

        self.herre = HerreClient(force_sync=True, config_path=config_path, auto_login=False)
        self.provisions = {}
        self.agent = QtAgent(self)
        self.agent.register(widgets={"rep": MY_TOP_REPRESENTATIONS}, on_provide=self.on_provide)(self.really_show)
        self.agent.register(widgets={
        "sample": SearchWidget(query="""
            query Search($search: String){
                options: samples(name: $search) {
                    value: id
                    label: name
                }
            }
        """)
    }, on_provide=self.on_provide)(self.upload)




    def on_provide(self, message: BouncedProvideMessage):
        self.provisions[message.meta.reference] = message
        self.provisionsWidget.clear()
        for key,value in self.provisions.items():
            self.provisionsWidget.addItem(f"Really Show used by {message.meta.context.user}")


    def really_show(self, rep: Representation):
        """Show Representaiton

        Shows a Dialog for the user to accept or not

        Args:
            rep (Representation): [description]
        """
        self.helper.open_as_layer(rep)

    def upload(self, name: str = None, sample: Sample = None) -> Representation:
        """Upload an Active Image

        Uploads the curently active image on Napari

        Args:
            name (str, optional): How do you want to name the image?
            sample (Sample, optional): Which sample should we put the new image in?

        Returns:
            Representation: The uploaded image from the app
        """
        array = self.helper.get_active_layer_as_xarray()
        return Representation.objects.from_xarray(array, name=name, sample=sample, tags=[])


    def login(self):
        if not self.herre.logged_in:
            self.herre.login()

            self.agent.provide(as_task=True)

            rep = Representation.objects.get(id=1)
            self.loginButton.setText(f"Logout {self.herre.user.username}")
        else:
            self.herre.logout()
            self.loginButton.setText("Login!")
            pass


    def close(self):
        # do stuff
        print("STUFFF HAPPENED THERE")
        self.herre.close()



   
