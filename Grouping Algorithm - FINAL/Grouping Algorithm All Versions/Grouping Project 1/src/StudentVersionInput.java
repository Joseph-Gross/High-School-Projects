import java.awt.SystemColor;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.util.ArrayList;

import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JPanel;

public class StudentVersionInput extends JPanel {

	private JLabel studentLabel;
	private JLabel choice1 = new JLabel("Choice 1: ");
	private JLabel choice2 = new JLabel("Choice 2: ");
	private JLabel choice3 = new JLabel("Choice 3: ");
	
	private JButton leftButton;
	private JButton rightButton;
	private JButton setStudentButton;
	
	private JComboBox<String> choice1ComboBox;
	private JComboBox<String> choice2ComboBox;
	private JComboBox<String> choice3ComboBox;
	
	private ArrayList<String> choiceList;
	private ArrayList<String> namesList;
	private ArrayList<Student> students;
	private ArrayList<String[]> choices;
	private int studentIndex=0;
	
	public StudentVersionInput(ArrayList<String> names) {
		namesList = names;
		studentLabel = new JLabel();
		
		students = new ArrayList<Student>();
		choices = new ArrayList<String[]>();
		
		choice1ComboBox = new JComboBox<String>();
		choice2ComboBox = new JComboBox<String>();
		choice3ComboBox = new JComboBox<String>();
		
		initializeStudents();
		setLabel();
		setComboBoxes();
		//createComboBoxes();
		createToggleButtons();
		createSetStudentButton();
		createChoices();
		createLayout();
	}
	
	public void createLayout() {
		this.setBounds(0, 60, 744, 418);
		this.setBackground(SystemColor.textHighlight);
		this.setLayout(null);
		
		//studentLabel.setFont(new Font("Monaco", Font.PLAIN, 13));
		studentLabel.setBounds(338, 23, 72, 20);
		this.add(studentLabel);
		
		rightButton.setBounds(401, 20, 61, 27);
		this.add(rightButton);
		
		leftButton.setBounds(268, 20, 61, 27);
		this.add(leftButton);
	
		//621, 383, 117
		setStudentButton.setBounds(550, 350, 150, 29);
		this.add(setStudentButton);
		
		choice1ComboBox.setBounds(295, 88, 164, 27);
		this.add(choice1ComboBox);
	
		choice2ComboBox.setBounds(295, 134, 164, 27);
		this.add(choice2ComboBox);
		
		choice3ComboBox.setBounds(295, 182, 164, 27);
		this.add(choice3ComboBox);
		
		//Font choices = new Font("Monaco", 13);
		
		//choice1.setFont(new Font("Arial", Font.PLAIN, 9);
		choice1.setBounds(190, 92, 93, 16);
		this.add(choice1);
		
		//choice2.setFont(new Font("Monaco", Font.PLAIN, 13));
		choice2.setBounds(190, 138, 93, 16);
		this.add(choice2);
		
		//choice3.setFont(new Font("Monaco", Font.PLAIN, 13));
		choice3.setBounds(190, 186, 93, 16);
		this.add(choice3);		
	}
	
	public void initializeStudents() {
		for(int i=0; i<namesList.size(); i++) {
			students.add(new Student(namesList, i));
		}
	}
	
	public void setLabel() {
		studentLabel.setText((students.get(studentIndex).name));
	}
	 
	public void setComboBoxes() {
		choiceList = students.get(studentIndex).getChoiceList();
		
		choice1ComboBox.removeAllItems();
		choice2ComboBox.removeAllItems();
		choice3ComboBox.removeAllItems();
		
		//Make one choice list for each student and have each combo box change with its own action listener
		
		for(String string: choiceList) {
			choice1ComboBox.addItem(string);
			choice2ComboBox.addItem(string);
			choice3ComboBox.addItem(string);
		}
		
		choice1ComboBox.setSelectedItem(students.get(studentIndex).choice1);
		choice2ComboBox.setSelectedItem(students.get(studentIndex).choice2);
		choice3ComboBox.setSelectedItem(students.get(studentIndex).choice3);
	}
	
	
	public void createToggleButtons() {
		leftButton = new JButton("<");
		ActionListener toggleLeft = new toggle(0);
		leftButton.addActionListener(toggleLeft);
		
		rightButton = new JButton(">");
		ActionListener toggleRight = new toggle(1);
		rightButton.addActionListener(toggleRight);
	}
	
	class toggle implements ActionListener {
		boolean right;
		
		public toggle(int n) {
			if(n==0) {
				right = false;
			} else {
				right = true;
			}
		}
		
		public void actionPerformed(ActionEvent event) {
			studentIndex = studentIndex % students.size();
			
			if(studentIndex == 0) {
				studentIndex = students.size();
			}
			
			if(right) {
				studentIndex++;
			} else {
				studentIndex--;
			}
			
			studentIndex = studentIndex % students.size();
			
			setLabel();
			setComboBoxes();
			setSetStudentChoices();
		}
	}
	
	public void setSetStudentChoices() {
		Student student = students.get(studentIndex);
		
		if(student.choiceSet == true) {
			setStudentButton.setText("Change Choices");
		} else {
			setStudentButton.setText("Confirm Choices");
		}
	}
	
	public void createSetStudentButton() {
		setStudentButton = new JButton("Confirm Choices");
		ActionListener setStudent = new setStudent();
		setStudentButton.addActionListener(setStudent);
	}
	
	class setStudent implements ActionListener {
		public void actionPerformed(ActionEvent event) {
			Student student = students.get(studentIndex);
			
			String choice1 = (String) choice1ComboBox.getSelectedItem();
			String choice2 = (String) choice2ComboBox.getSelectedItem();
			String choice3 = (String) choice3ComboBox.getSelectedItem();
			
			student.setChoice1(choice1);
			student.setChoice2(choice2);
			student.setChoice3(choice3);
			
			student.choiceSet();
			
			updateChoices(student);
			StudentVersionTable.updateData(choices.get(studentIndex), studentIndex);
		}
	}
	
	public void createChoices() {
		for(int i=0; i<students.size(); i++) {
			choices.add(createChoice(students.get(i)));
		}
	}
	
	public void updateChoices(Student student) {
		if(contains(choices, student.name)) {
			for(String[] element: choices) {
				if(element[0].equalsIgnoreCase(student.name)) {
					element[1] = student.choice1; 
					element[2] = student.choice2;
					element[3] = student.choice3;
					break;
				}
			}
		} else {
			choices.add(createChoice(student));
		}
	}
	
	public boolean contains(ArrayList<String[]> a, String name) {
		boolean contains = false;
		
		for(String[] element: a) {
			if(element[0].equalsIgnoreCase(name)) {
				contains = true;
			}
		}
		
		return contains;
	}
	
	public String[] createChoice(Student student) {
		String[] choice = new String[4];
		choice[0] = student.name;
		choice[1] = student.choice1; 
		choice[2] = student.choice2;
		choice[3] = student.choice3;
		return choice;
	}

	public ArrayList<String[]> getChoices() {
		return choices;
	}

	
}
