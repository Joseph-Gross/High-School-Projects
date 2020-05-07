import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.SystemColor;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.FileNotFoundException;
import java.util.ArrayList;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextArea;

public class StudentVersionTable extends JPanel{
	
	private JTable studentTable;
	private JButton submitButton;
	private static ArrayList<String[]> choices;
	static Object[][] studentData;
	
	
	private int[][] initialInput;
	private ArrayList<String> names;
	
	private JTextArea outputArea;
	private ArrayList<String> result;
	
	public StudentVersionTable(ArrayList<String[]> choicesInput, ArrayList<String> namesInput) {
		choices = choicesInput;
		names = namesInput;
		createInitialInput();
		createTablePanel();
	}

	public void createTablePanel() {
		createTable();
		createSubmitButton();
		this.setBackground(SystemColor.textHighlight);
	}
	
	private void createSubmitButton() {
		submitButton = new JButton("Submit");
		ActionListener submitListener = new Submit();
		submitButton.addActionListener(submitListener);
		
		this.add(submitButton);
	}
	
	class Submit implements ActionListener {
		public void actionPerformed(ActionEvent event) {
//			for(String[] element: choices) {
//				System.out.print(element[0] + ": ");
//				System.out.print(element[1] + " ");
//				System.out.print(element[2] + " ");
//				System.out.print(element[3]);
//				System.out.println();
//				setInitialInput(element);
//			}
//			
//			for(int i=0; i<initialInput.length; i++) {
//				for(int j=0; j<initialInput.length; j++) {
//					System.out.print(initialInput[i][j]);
//				}
//				System.out.println();
//			}
			
			for(String[] element: choices) {
				setInitialInput(element);
			}
			
			try {
				new DubardAlgorithm2(initialInput, names);
				result = DubardAlgorithm2.getCorrectGrouping();
		   } catch (FileNotFoundException e) {
			   e.printStackTrace();
		   }
			createFinalFrame();
			submitButton.setEnabled(false);
		}
	}

	public void createTable() {
		String[] header = {"Student Name", "Choice 1", "Choice 2", "Choice 3"};
		createStudentData(choices);
		
		studentTable = new JTable(studentData, header);
		studentTable.setPreferredScrollableViewportSize(new Dimension (500,400));
		studentTable.setFillsViewportHeight(true);
		studentTable.setShowVerticalLines(true);
		studentTable.setGridColor(Color.BLACK);
		
		JScrollPane scrollPane = new JScrollPane(studentTable);
		this.add(scrollPane);
	}
	
	public void createStudentData(ArrayList<String[]> choicesInput) {
		studentData = new Object[choicesInput.size()][4];
		
		for(int i=0; i<studentData.length; i++) {
			studentData[i] = choicesInput.get(i);
		}
	}

	public static void updateData(String[] newData, int studentIndex) {
		studentData[studentIndex] = newData;
		
		choices.get(studentIndex)[1] = newData[1];
	}

	public void createInitialInput() {
		initialInput = new int[names.size()][names.size()];
		
		for(int i=0; i<initialInput.length; i++) {
			for(int j=0; j<initialInput.length; j++) {
				initialInput[i][j] = 0;
			}
		}
	}
	
	public void setInitialInput(String[] student) {
		if(!student[1].equals("none")) {
			initialInput[getIndex(student[0], names)][getIndex(student[1], names)] = 3;
		}
		if(!student[2].equals("none")) {
			initialInput[getIndex(student[0], names)][getIndex(student[2], names)] = 2;
		}
		if(!student[3].equals("none")) {
			initialInput[getIndex(student[0], names)][getIndex(student[3], names)] = 1;
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
