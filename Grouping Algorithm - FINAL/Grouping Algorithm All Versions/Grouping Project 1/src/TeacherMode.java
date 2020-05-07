import javax.swing.*;
import java.util.*;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.SystemColor;
import java.awt.event.*;
import java.io.FileNotFoundException;

public class TeacherMode implements ActionListener {

	private JFrame frame;
	private JPanel bigPanel;
	private JScrollPane scroll;
	private JButton enter = new JButton("ENTER CHOICES");
	public ArrayList<String> studentNames = new ArrayList<String>();
	public int numStudes;
	public ArrayList<StudentPanel> panelList;
	public ArrayList<StudentTeacher> students = new ArrayList<StudentTeacher>();
	public ArrayList<String[]> resultArray;

	private int[][] initialInput;
	private JTextArea outputArea;
	private ArrayList<String> result;
	
	public TeacherMode(ArrayList<String> input) {
		//studentNames.add("RESET LIST");
		input.add(0, "none");
		studentNames = input;
		numStudes = studentNames.size()-1;
		resultArray = new ArrayList<String[]>();
		enter.addActionListener(this);
		initialize();
		createStudentObjects();
		createPanels();
	}

	private void initialize() {
		frame = new JFrame("TEACHER MODE");
		frame.setBounds(230, 60, 800, 700);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getContentPane().setLayout(null);
		frame.setVisible(true);
		bigPanel = new JPanel();
		bigPanel.setLayout(null);
		bigPanel.setPreferredSize(new Dimension(1000, (numStudes+2)*100));
		bigPanel.setBackground(SystemColor.textHighlight);
		scroll = new JScrollPane(bigPanel, JScrollPane.VERTICAL_SCROLLBAR_ALWAYS, JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);
		scroll.setBounds(0, 0, 800, 700);
		scroll.setVisible(true);
		frame.add(scroll);
		
		JLabel firstChoicelbl = new JLabel("FIRST CHOICE");
		JLabel secondChoicelbl = new JLabel("SECOND CHOICE");
		JLabel thirdChoicelbl = new JLabel("THIRD CHOICE");
		firstChoicelbl.setBounds(230, 26, 100, 40);
		secondChoicelbl.setBounds(415, 26, 100, 40);
		thirdChoicelbl.setBounds(600, 26, 100, 40);
		bigPanel.add(firstChoicelbl);
		bigPanel.add(secondChoicelbl);
		bigPanel.add(thirdChoicelbl);
		

	}
	
	private void createStudentObjects(){
		for(int x = 0; x < numStudes; x++){
			students.add(new StudentTeacher(studentNames, x+1));
		}
		for(int x = 0; x <numStudes; x++){
			//students.get(x).setChoice1List();
			//students.get(x).setChoice2List();
			//students.get(x).setChoice3List();
		}
	}
	
	private void createPanels(){
		panelList = new ArrayList<StudentPanel>();
		for(int x = 0; x < numStudes; x++){
			panelList.add(new StudentPanel(students.get(x)));
		}
		for(int x = 0; x < numStudes; x++){
			bigPanel.add(panelList.get(x).panel);
			}
		enter.setBounds(354, StudentPanel.y +20, 189, 43);
		bigPanel.add(enter);
	}

	@Override
	public void actionPerformed(ActionEvent event) {
		if(event.getSource().equals(enter)){
			for(int x = 0; x < numStudes; x++){
				String[] temp = new String[4];
				temp[0] = panelList.get(x).student.name;
				temp[1] = (String) panelList.get(x).firstChoiceList.getSelectedItem();
				temp[2] = (String) panelList.get(x).secondChoiceList.getSelectedItem();
				temp[3] = (String) panelList.get(x).thirdChoiceList.getSelectedItem();
				resultArray.add(temp);
			}
			
			studentNames.remove(0);
			
			createInitialInput();
			for(String[] element: resultArray) {
				setInitialInput(element);
			}
			
			try {
				new DubardAlgorithm2(initialInput, studentNames);
				result = DubardAlgorithm2.getCorrectGrouping();
		   } catch (FileNotFoundException e) {
			   e.printStackTrace();
		   }
			createFinalFrame();
			enter.setEnabled(false);
		}
	}
	
	public void createInitialInput() {
		initialInput = new int[studentNames.size()][studentNames.size()];
		
		for(int i=0; i<initialInput.length; i++) {
			for(int j=0; j<initialInput.length; j++) {
				initialInput[i][j] = 0;
			}
		}
	}
	
	public void setInitialInput(String[] student) {
		if(!student[1].equals("none")) {
			initialInput[getIndex(student[0], studentNames)][getIndex(student[1], studentNames)] = 3;
		}
		if(!student[2].equals("none")) {
			initialInput[getIndex(student[0], studentNames)][getIndex(student[2], studentNames)] = 2;
		}
		if(!student[3].equals("none")) {
			initialInput[getIndex(student[0], studentNames)][getIndex(student[3], studentNames)] = 1;
		}
	}
	
	public int getIndex(String name, ArrayList<String> names) {
		return names.indexOf(name);
	}
	
	public void createFinalFrame() {
		JFrame finalFrame = new JFrame("Dubard's Difficult Dilemma");
		JPanel outputPanel = new JPanel();
		JLabel outputLabel = new JLabel("Optimized Pairings");
		
		createTextArea();
		JScrollPane scrollPane = new JScrollPane(outputArea);

		outputPanel.setBackground(new Color(221,160,221));
		outputPanel.add(outputLabel, BorderLayout.PAGE_START);
		outputPanel.add(scrollPane, BorderLayout.CENTER);

		finalFrame.setTitle("Dubard's Difficult Dilemma");
		finalFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		finalFrame.setBounds(300, 150, 385, 550);
		finalFrame.add(outputPanel);
		finalFrame.setResizable(false);
		finalFrame.setVisible(true); 
	}
	
	private void createTextArea() {
		outputArea = new JTextArea(25, 25);
		outputArea.setEditable(false);
		outputArea.setText("");
		
		for(int i=0; i<result.size(); i++) {
			outputArea.append("Pair " + (i+1) + ": " + result.get(i) + "\n");
		}
	}

	
}