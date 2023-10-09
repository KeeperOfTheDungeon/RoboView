import customtkinter as ctk

from Devices.LegSensors.LegSensors import LegSensors
from RoboControl.Robot.AbstractRobot.AbstractListener import SetupListener
from RoboControl.Robot.Component.Sensor.vcnl4000.Vcnl4000 import Vcnl4000
from RoboView.Robot.Device.Viewer.DeviceView import DeviceView
from RoboView.Robot.component.view.ComponentSetupView import ComponentSetupView
from RoboView.Robot.component.view.ComponentView import ComponentView

AVERAGING_TEXT = "averaging"
AUTO_COMPENSATION_TEXT = "auto offset"
AUTO_CONVERSION_TEXT = "auto conversion"
FREQUENCY_TEXT = "IR frequency"
IR_CURRENT_TEXT = "IR current"
CALIBRATION_TEXT = "calibration"
CMD_CALIBRATION = "cmdCalibration"
WRITE_TEXT = "write"
FETCH_TEXT = "fetch"
EXPORT_TEXT = "export"
CMD_IMPORT = "cmdImport"
IMPORT_TEXT = "import"
CMD_EXPORT = "cmdExport"

WIDTH: int = 310
HEIGHT: int = 105
HEIGHT_CALIBRATION: int = 270


class Vcnl4000SetupView(ComponentSetupView, SetupListener):
    FRAME_NAME: str = "Leg Controller Setup"
    _device: LegSensors

    def __init__(self, root, component: Vcnl4000, settings_key):
        super().__init__(root, component, settings_key, 250, 120)
        self._component: Vcnl4000 = component

        self._current_selector: ctk.CTkComboBox = None  # Vcnl4000IrCurrent
        self._averaging_selector: ctk.CTkComboBox = None  # Vcnl4000AveragingModes
        self._frequency_selector: ctk.CTkComboBox = None  # Vcnl4000FrequencyModes

        self._auto_conversion: ctk.CTkComboBox = None
        self._auto_compensation: ctk.CTkComboBox = None

        self._calibration: bool = False

        # showCalibrationMenueItem: JMenuItem
        # self._distance_table_view: Vcnl4000DistanceTable = Vcnl4000DistanceTable()

        self.build_view()
        self._component.add_setup_listener(self)
        self._component.get_distance_sensor().add_setup_listener(self)

    def build_view(self) -> None:
        super().build_view()

        """
        Insets insets = this.getBorder().getBorderInsets(this);
        description = new JLabel(Vcnl4000SetupView.AVERAGING_TEXT);
        description.setBounds(insets.left+130,insets.top+5,80,22);
        this.add(description);
        
        this.averagingSelector = new JComboBox<Vcnl4000AveragingModes>();
        
        for(Vcnl4000AveragingModes rate : Vcnl4000AveragingModes.values())
        {
            this.averagingSelector.addItem(rate);
        }
        this.averagingSelector.setBounds(insets.left+200,insets.top+5,110,22);
        this.add(this.averagingSelector);
        
        this.autoCompensationCheckBox = new JCheckBox(AUTO_COMPENSATION_TEXT);
        this.autoCompensationCheckBox.setBounds(insets.left+5,insets.top+5,110,22);
        this.add(this.autoCompensationCheckBox);
        
        this.autoConversionCheckBox = new JCheckBox(AUTO_CONVERSION_TEXT);
        this.autoConversionCheckBox.setBounds(insets.left+5,insets.top+30,110,22);
        this.add(this.autoConversionCheckBox);
        
        description = new JLabel(Vcnl4000SetupView.IR_CURRENT_TEXT);
        description.setBounds(insets.left+130,insets.top+30,80,22);
        this.add(description);
    
        this.currentSelector = new JComboBox<Vcnl4000IrCurrent>();
        
        for(Vcnl4000IrCurrent current : Vcnl4000IrCurrent.values())
        {
            this.currentSelector.addItem(current);
        }
        this.currentSelector.setBounds(insets.left+200,insets.top+30,110,22);
        this.add(this.currentSelector);
        
        description = new JLabel(Vcnl4000SetupView.FREQUENCY_TEXT);
        description.setBounds(insets.left+130,insets.top+55,80,22);
        this.add(description);
         
        this.frequencySelector = new JComboBox<Vcnl4000FrequencyModes>();
        for(Vcnl4000FrequencyModes frequency : Vcnl4000FrequencyModes.values())
        {
            this.frequencySelector.addItem(frequency);
        }
        this.frequencySelector.setBounds(insets.left+200,insets.top+55,110,22);
        this.add(this.frequencySelector);
        
        this.addSetButton(insets.left+5, insets.top+55, 50, 22);
        this.addGetButton(insets.left+60, insets.top+55, 50, 22);
        
        this.addSaveButton(insets.left+5, insets.top+80, 50, 22);
        this.addLoadButton(insets.left+60, insets.top+80, 50, 22);
    
        if (this.calibration)
            this.addCalibrationView(insets);
        """

    def add_calibration_view(self, insets: "Insets") -> None:
        raise ValueError("WIP: add_calibration_view")
        """
        int index;
        
        this.distanceTableView= new Vcnl4000DistanceTable();
        distanceTableView.setBounds(insets.left+5, insets.top+105, 200, 155);
        this.add(distanceTableView);
        
        JButton tmpButton;
        
        for (index =0; index<8 ;index++)
        {
            tmpButton = new JButton("\u21BB");
            tmpButton.setBounds(insets.left+205, insets.top+129+index*16, 30, 16);
            tmpButton.setBorder(new LineBorder(Color.GRAY));
            tmpButton.setActionCommand(""+index);
            tmpButton.addActionListener(new ActionListener(){
                
                @Override
                public void actionPerformed(ActionEvent actionEvent)
                {
                    
                    try
                    {
                        Vcnl4000SetupView.this.component.remote_getRawProximityValue();
                        Thread.sleep(100);
                        
                        Vcnl4000SetupView.this.distanceTableView.getDistanceTable().setProximityValue(
                                    Integer.valueOf(actionEvent.getActionCommand()), 
                                    Vcnl4000SetupView.this.component.getDistanceSensor().getProximityValue());
                        
                        Vcnl4000SetupView.this.distanceTableView.invalidate();
                        Vcnl4000SetupView.this.distanceTableView.repaint();
                    } catch (InterruptedException e)
                    {
                        // TODO Auto-generated catch block
                        e.printStackTrace();
                    }
                }
                
            });
            this.add(tmpButton);
        }
        
        
        
        
        tmpButton = new JButton(Vcnl4000SetupView.WRITE_TEXT);
        tmpButton.setBounds(insets.left+245, insets.top+105, 60, 25);
        tmpButton.addActionListener(new ActionListener(){
    
            @Override
            public void actionPerformed(ActionEvent arg0)
            {
                Vcnl4000SetupView.this.component.remote_setDistanceTable(Vcnl4000SetupView.this.distanceTableView.getDistanceTable());;
            }
            
        });
        this.add(tmpButton);
        tmpButton.setBorder(new LineBorder(Color.GRAY));
        this.add(tmpButton);
        
        
    
        tmpButton = new JButton(Vcnl4000SetupView.FETCH_TEXT);
        tmpButton.setBounds(insets.left+245, insets.top+130, 60, 25);
        tmpButton.addActionListener(new ActionListener(){
    
            @Override
            public void actionPerformed(ActionEvent arg0)
            {
                Vcnl4000SetupView.this.component.remote_getDistanceTable();
            }
            
        });
        tmpButton.setBorder(new LineBorder(Color.GRAY));
        this.add(tmpButton);
        
        tmpButton = new JButton(Vcnl4000SetupView.EXPORT_TEXT);
        tmpButton.setBounds(insets.left+245, insets.top+155, 60, 25);
        tmpButton.addActionListener(new ActionListener(){
    
            @Override
            public void actionPerformed(ActionEvent arg0)
            {
                Vcnl4000SetupView.this.exportDistanceTable();
            }
            
        });
        tmpButton.setBorder(new LineBorder(Color.GRAY));
        this.add(tmpButton);
        
        
        tmpButton = new JButton(Vcnl4000SetupView.IMPORT_TEXT);
        tmpButton.setBounds(insets.left+245, insets.top+180, 60, 25);
        tmpButton.setActionCommand(Vcnl4000SetupView.CMD_IMPORT);
        tmpButton.addActionListener(this);
        tmpButton.setBorder(new LineBorder(Color.GRAY));
        this.add(tmpButton);	
        """

    # //protected static final Object [] [] DISTANCE_TABLE_COLLUMNS = {{"distance",new CsvDataInteger()},{"value", new CsvDataInteger()}};

    def export_distance_table(self) -> None:
        raise ValueError("WIP export_distance_table")
        """
        Object [] dataRow = new Object[2];
        
        //	CsvHeadRow csvHead = new CsvHeadRow();
        //	
        //	csvHead.addColumn("test",new CsvDataInteger(0));
        //	csvHead.addColumn("test2",new CsvDataInteger(0));
        //	
        //	Csv csv = new Csv(csvHead);
        //
        //	DistanceTable distanceTable;
        //	
        //	
        //	
        //	distanceTable = this.distanceTableView.getDistanceTable();
        //	
        //	int index;
        //	
        //	index=0;
        //	
        //	// for
        //	dataRow[0] = new CsvDataInteger(distanceTable.getDistance(index));
        //	dataRow[1] = new CsvDataInteger(distanceTable.getProximityValue(index));
        //	csv.addDataRow(dataRow);
        //	
        //	
        //	
        //	csv.write();
        """

    def get_view_width(self) -> int:
        return WIDTH

    def get_view_height(self) -> int:
        if self._calibration:
            return HEIGHT_CALIBRATION
        return HEIGHT

    def make_popup_menu(self) -> None:
        super().make_popup_menu()
        # this.showCalibrationMenueItem = this.addCheckBoxMenuItem(this.contextMenue , Vcnl4000SetupView.CALIBRATION_TEXT, Vcnl4000SetupView.CMD_CALIBRATION);

    def update(self) -> None:
        self._current_selector.set_selection(self._component.get_ir_current())
        self._averaging_selector.set_selection(self._component.get_averaging())
        self._frequency_selector.set_selection(self._component.get_proximity_frequency())
        self._auto_conversion.set_selection(self._component.get_auto_conversion())
        self._auto_compensation.set_selection(self._component.get_auto_compensation())

    def set_settings(self) -> bool:
        self._component.remote_set_settings(
            self._averaging_selector.get(),
            self._frequency_selector.get(),
            self._current_selector.get(),
            self._auto_conversion.get(),
            self._auto_compensation.get(),
        )
        return False

    # @staticmethod
    # def create_view(sensor: Vcnl4000) -> ComponentView:
    #     if sensor is not None:
    #         return Vcnl4000SetupView(sensor)
    #     else:
    #         return MissingValueView(Vcnl4000.__class__.__name__)

    def settings_changed(self, component: "RobotComponent") -> None:
        self.update()

    def action_performed(self, event: "ActionEvent") -> None:
        cmd = event.get_action_command()
        if cmd == Vcnl4000SetupView.CMD_CALIBRATION:
            self._calibration = self.showCalibrationMenueItem.isSelected()
            self.build_view()
        else:
            print(cmd)
            super().action_performed(event)

    def distance_table_changed(self, sensor: "Vcnl4000DistanceSensor") -> None:
        self._distance_table_view.set_distance_table(sensor.get_distance_table())
