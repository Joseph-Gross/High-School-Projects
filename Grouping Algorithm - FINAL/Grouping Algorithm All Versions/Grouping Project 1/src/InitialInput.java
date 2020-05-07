import java.awt.BorderLayout;
import java.awt.SystemColor;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;

import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;

public class InitialInput extends JPanel {

	private ArrayList<String> names = new ArrayList<String>();

	private JLabel nameLabel;
	private JTextField nameField;
	private JButton addName;
	private JButton student;
	private JButton restart;
	private JButton teacher;
	
	private static final int height = 25;
	private static final int length = 25;
	
	private JTextArea resultArea;

	public InitialInput() {
		resultArea = new JTextArea(height, length);
		resultArea.setText("");
		resultArea.setEditable(true);
		
		createTextField();
		createButton();
		createPanel();
		this.setBackground(SystemColor.textHighlight);
	}
	
	private void createTextField() {
		final int fieldWidth = 10;
		
		nameLabel = new JLabel("Enter Name: ");
		nameField = new JTextField(fieldWidth);
		nameField.setText("");
	}
	
	private void createButton() {
		addName = new JButton("Add Name");
		ActionListener nameListener = new addName();
		addName.addActionListener(nameListener);
		
		student = new JButton("Student Version");
		ActionListener studentListener = new StudentVersionListener();
		student.addActionListener(studentListener);
		
		restart = new JButton("Restart");
		ActionListener restartListener = new restart();
		restart.addActionListener(restartListener);
		
		teacher = new JButton("Teacher Version");
		ActionListener teacherListener = new TeacherVersionListener();
		teacher.addActionListener(teacherListener);
	}
	
	class addName implements ActionListener {
		public void actionPerformed(ActionEvent event) {
			String nameInput = nameField.getText();
			resultArea.append(nameInput + "\n");
			nameField.setText("");
		}
	}
		
	class StudentVersionListener implements ActionListener {
		public void actionPerformed(ActionEvent event) {
			resultArea.setEditable(false);
			addName.setEnabled(false);
			student.setEnabled(false);
			teacher.setEnabled(false);
			for (String line : resultArea.getText().split("\\n")) {
				names.add(line);
			}
			new StudentVersion(names);
		}
	}
	
	class restart implements ActionListener {
		public void actionPerformed(ActionEvent event) {
			resultArea.setText("");
			resultArea.setEditable(true);
			addName.setEnabled(true);
			student.setEnabled(true);
			teacher.setEnabled(true);
			names = new ArrayList<String>();
		}
	}
	
	class TeacherVersionListener implements ActionListener {
		public void actionPerformed(ActionEvent event) {
			resultArea.setEditable(false);
			addName.setEnabled(false);
			student.setEnabled(false);
			teacher.setEnabled(false);
			for (String line : resultArea.getText().split("\\n")) {
				names.add(line);
			}
			new TeacherMode(names);
		}
	}
	
	private void createPanel() {
		JPanel namePanel = new JPanel();
		
		namePanel.add(nameLabel);
		namePanel.add(nameField);
		namePanel.add(addName);
		namePanel.setBackground(SystemColor.textHighlight);
		
		add(namePanel, BorderLayout.PAGE_START);
		
		JScrollPane scrollPane = new JScrollPane(resultArea);
		add(scrollPane, BorderLayout.CENTER);
		
		add(student, BorderLayout.PAGE_END);
		add(teacher, BorderLayout.PAGE_END);
		add(restart, BorderLayout.PAGE_END);
	}
}


	
