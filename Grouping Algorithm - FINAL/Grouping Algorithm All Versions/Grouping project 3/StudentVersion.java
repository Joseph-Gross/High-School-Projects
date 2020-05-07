import java.awt.event.KeyEvent;
import java.util.ArrayList;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JTabbedPane;
import javax.swing.UIManager;

public class StudentVersion {
	
	private JFrame frame;
	private JTabbedPane tabbedPane;
	private ArrayList<String> namesList;
	
	public StudentVersion(ArrayList<String> names) {
		namesList = names;
		createTabbedPane();
		
		frame = new JFrame();
		frame.setTitle("Student Version1");
		frame.getContentPane().setBackground(UIManager.getColor("ComboBox.disabledForeground"));
		frame.setBounds(300, 175, 750, 500);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.add(tabbedPane);
		frame.setVisible(true); 
		frame.setResizable(false); 
	}
	
	public void createTabbedPane(){
		tabbedPane = new JTabbedPane();
		
		JPanel input = new StudentVersionInput(namesList);
        tabbedPane.addTab("Student Input", input);
        tabbedPane.setMnemonicAt(0, KeyEvent.VK_1);
         
        JPanel input2 = new StudentVersionTable(((StudentVersionInput) input).getChoices(), namesList);
        tabbedPane.addTab("Teacher View", input2);
        tabbedPane.setMnemonicAt(0, KeyEvent.VK_1);
	}
}
