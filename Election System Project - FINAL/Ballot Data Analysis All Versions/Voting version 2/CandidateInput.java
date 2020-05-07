import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.SystemColor;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;

public class CandidateInput extends JPanel {

	private JFrame frame;
	private JLabel nameLabel;
	private JTextField nameField;
	private JButton addName;
	private JButton submitButton;
	
	private static final int height = 25;
	private static final int length = 25;
	
	private JTextArea resultArea;
	private ArrayList<String> candidateNames;

	public CandidateInput(ArrayList<String> candidateNames) {
		this.candidateNames = candidateNames;
		resultArea = new JTextArea(height, length);
		resultArea.setText("");
		resultArea.setEditable(true);
		
		createTextField();
		createButton();
		createPanel();
		this.setBackground(new Color(132, 193, 247));
		
		frame = new JFrame();
		frame.setTitle("Candidate Data");
		frame.getContentPane().setBackground(new Color(221,160,221));
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setBounds(460, 160, 385, 550);
		frame.add(this);
		frame.setResizable(false);
		frame.setVisible(true); 
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

		submitButton = new JButton("Submit");
		ActionListener submitListener = new Submit();
		submitButton.addActionListener(submitListener);
	}
	
	class addName implements ActionListener {
		public void actionPerformed(ActionEvent event) {
			String nameInput = nameField.getText();
			resultArea.append(nameInput + "\n");
			nameField.setText("");
		}
	}
	
	class Submit implements ActionListener {
		public void actionPerformed(ActionEvent event) {
			
			for (String line : resultArea.getText().split("\\n")) {
				candidateNames.add(line);
			}
			
			//System.out.println(names);
			frame.dispose();
		}
	}
	
	private void createPanel() {
		JPanel namePanel = new JPanel();
		
		namePanel.add(nameLabel);
		namePanel.add(nameField);
		namePanel.add(addName);
		namePanel.setBackground(new Color(132, 193, 247));
		
		add(namePanel, BorderLayout.PAGE_START);
		
		JScrollPane scrollPane = new JScrollPane(resultArea);
		add(scrollPane, BorderLayout.CENTER);
		
		add(submitButton, BorderLayout.PAGE_END);
	}
}


	
