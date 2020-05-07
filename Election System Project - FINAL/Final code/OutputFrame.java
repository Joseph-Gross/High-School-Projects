import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSpinner;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.SpinnerModel;
import javax.swing.SpinnerNumberModel;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

public class OutputFrame extends JFrame{
	private static final long serialVersionUID = 5436246181951685074L;

	private JTextArea outputArea;
	
	private JButton openButton;
	private JButton candidatesButton;
	private JButton saveButton;
	private JButton runButton;
	private JButton clearButton;
	private JFrame finalFrame;
	private JSpinner spinner;
	
	private JLabel saveLabel;
	private JTextField nameField;
	private JLabel winningCandidatesLabel;
	
	private String filePath;
	private int numberOfWinners;
	private ArrayList<String> candidateNames;
	
	
	public OutputFrame() {
		candidateNames = new ArrayList<String>();
		saveLabel = new JLabel();
		filePath = "";
		
		finalFrame = new JFrame("Student Government Elections");
		JPanel outputPanel = new JPanel();
		
		createTextArea();
		JScrollPane scrollPane = new JScrollPane(outputArea);

		createSpinner();
		createSaveButton();
		createOpenButton();
		createCandidatesButton();
		createNameField();
		createRunButton();
		createClearButton();
		createWinningCandidatesLabel();
		
		outputPanel.setBackground(new Color(221,160,221));
		outputPanel.add(winningCandidatesLabel,  BorderLayout.PAGE_START);
		outputPanel.add(spinner, BorderLayout.PAGE_START);
		outputPanel.add(candidatesButton, BorderLayout.PAGE_START);
		outputPanel.add(openButton, BorderLayout.PAGE_START);
//		outputPanel.add(runButton, BorderLayout.PAGE_START);
		outputPanel.add(clearButton, BorderLayout.PAGE_START);
		outputPanel.add(scrollPane, BorderLayout.CENTER);
		outputPanel.add(saveButton);
		outputPanel.add(nameField);
		outputPanel.add(saveLabel);

		finalFrame.setTitle("Student Government Elections");
		finalFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		finalFrame.setBounds(370, 130, 558, 625);
		finalFrame.add(outputPanel);
		finalFrame.setResizable(true);
		finalFrame.setVisible(true); 
	}
	
	public void createWinningCandidatesLabel() {
		winningCandidatesLabel = new JLabel("Number of winners: ");
	}
	
	public void createSpinner() {
		numberOfWinners = 1;
		SpinnerModel spinnerModel = new SpinnerNumberModel(1, 1, 100, 1);
		spinner = new JSpinner(spinnerModel);
		spinner.addChangeListener(new ChangeListener() {
			public void stateChanged(ChangeEvent e) {
				numberOfWinners = (int) ((JSpinner)e.getSource()).getValue();
			}
		});
	}
	
	public void createNameField() {
		final int fieldWidth = 10;
		
		nameField = new JTextField(fieldWidth);
		nameField.setText("");
	}
	
	public void createTextArea() {
		outputArea = new JTextArea(30, 42);
		outputArea.setEditable(false);
		outputArea.setText("");
	}
	
	public void setTextAreaData(ArrayList<Candidate> winningCandidates, 
			ArrayList<Candidate> candidates, ArrayList<ArrayList<String>> master, 
			ArrayList<ArrayList<String>> allData) {
		
		outputArea.append("Winning Candidate(s): \n");
		for(Candidate candidate: winningCandidates) {
			outputArea.append(candidate.name + "\n");
		}
		
		outputArea.append("\nAll Candidates: \n");
		for(Candidate candidate: candidates) {
			outputArea.append(candidate.name + "\n");
		}
		
		outputArea.append("\nAll Ballots: \n");
		int counter = 1;
		for(ArrayList<String> vote: master) {
			String voteData = "";
			for(int i=0; i<vote.size()-1; i++) {
				voteData += vote.get(i) + ", ";
			} voteData += vote.get(vote.size()-1);
			
			outputArea.append(counter + ": " + voteData + "\n");
			counter++;
		}
		
		outputArea.append("\n\n\nElection Data: \n\n");
		for(int i=allData.size(); i>0; i--) {
			ArrayList<String> round = allData.get(i-1);
			for(String line: round) {
				outputArea.append(line + "\n");
			}
			outputArea.append("\n\n");
		}
	
		outputArea.append("\n----------------------");
		outputArea.append("-------------------------");
		outputArea.append("-------------------------\n");
	}
	
	
	
	public void createClearButton() {
		clearButton = new JButton("Clear");
		clearButton.addActionListener(new Clear());
	}
	
	class Clear implements ActionListener {
		public void actionPerformed(ActionEvent e) {
			outputArea.setText("");
			openButton.setEnabled(false);
			candidatesButton.setEnabled(true);
			Round.roundNumber = 1;
			Round.allData = new ArrayList<ArrayList<String>>();
			candidateNames.clear();
		}
	}
	
	
	public void createRunButton() {
		runButton = new JButton("Run");
		runButton.addActionListener(new Run());
	}
	
	class Run implements ActionListener {
		public void actionPerformed(ActionEvent e) {
			TestData test = null; 
	        
			try {
				test = new TestData(filePath + ".txt", candidateNames);
			} catch (FileNotFoundException e1) {
				try {
					test = new TestData(filePath, candidateNames);
				} catch (FileNotFoundException e2) {
					e2.printStackTrace();
			}
			e1.printStackTrace();
		}
			double[] voteCounts = new double[test.getCandidates().size()];
			for(int i=0; i<voteCounts.length; i++) {
				voteCounts[i] = 0;
			}
			
			Round round = new Round(test.getMaster(), test.getCandidates(), new ArrayList<Candidate>(), numberOfWinners, voteCounts);
			setTextAreaData(round.winningCandidates, test.getCandidates(), test.getRawBallotData(), round.getAllData());
		}
	}
	
	
	public void createOpenButton() {
		openButton = new JButton("Ballot Data");
		openButton.addActionListener(new Open());
		openButton.setEnabled(false);
	}
	
	class Open implements ActionListener {
		public void actionPerformed(ActionEvent e) {
			JFileChooser fileChooser = new JFileChooser();
			fileChooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
			int rVal = fileChooser.showDialog(finalFrame, "Open File");
			if (rVal == JFileChooser.APPROVE_OPTION) {
				String path = fileChooser.getSelectedFile().getAbsolutePath() + ".txt";
		        System.out.println(path);

		        filePath = fileChooser.getSelectedFile().getAbsolutePath();
		        TestData test = null; 
		        
				try {
					test = new TestData(path, candidateNames);
				} catch (FileNotFoundException e1) {
					path = fileChooser.getSelectedFile().getAbsolutePath();
					try {
						test = new TestData(path, candidateNames);
					} catch (FileNotFoundException e2) {
						e2.printStackTrace();
					}
					e1.printStackTrace();
				}
				
				double[] voteCounts = new double[test.getCandidates().size()];
				for(int i=0; i<voteCounts.length; i++) {
					voteCounts[i] = 0;
				}

				Round round = new Round(test.getMaster(), test.getCandidates(), new ArrayList<Candidate>(), numberOfWinners, voteCounts);
				setTextAreaData(round.winningCandidates, test.getCandidates(), test.getRawBallotData(), round.getAllData());
				openButton.setEnabled(false);
			} 
			if (rVal == JFileChooser.CANCEL_OPTION) {
				openButton.setEnabled(true);
			}	
		}
	}
	
	
	public void createCandidatesButton() {
		candidatesButton = new JButton("Candidates");
		candidatesButton.addActionListener(new CandidateInputListener());
	}
	
	class CandidateInputListener implements ActionListener {
		public void actionPerformed(ActionEvent e) {
			new CandidateInput(candidateNames);
			openButton.setEnabled(true);
			candidatesButton.setEnabled(false);
		}
	}
	
	
	public void createSaveButton() {
		saveButton = new JButton("Save results as");
		saveButton.addActionListener(new Save());
	}
	
	class Save implements ActionListener {
		public void actionPerformed(ActionEvent e) {
			JFileChooser fileChooser = new JFileChooser();
			fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
			int rVal = fileChooser.showDialog(finalFrame, "Save File");
			if (rVal == JFileChooser.APPROVE_OPTION) {
				String path = fileChooser.getSelectedFile().getPath();
		        System.out.println(path);
		        saveLabel.setText("Data has been saved");
		        try {
		        	if(nameField.getText().equals("")) {
		        		nameField.setText("default");
		        	}
		        	saveToFile(path, nameField.getText(), true);
					saveToFile(path, nameField.getText(), false);
				} catch (IOException e1) {
					e1.printStackTrace();
				}
		        saveButton.setEnabled(false);
			} 
			if (rVal == JFileChooser.CANCEL_OPTION) {
				saveLabel.setText("Cancelled");
				saveButton.setEnabled(true);
			}	
		}
	}

	
	public void saveToFile(String directoryPath, String name, Boolean macintosh) throws IOException {
		BufferedWriter writer;
		
		if(macintosh) {
		    writer = new BufferedWriter(new FileWriter(new File(directoryPath + "/" + name)));
		} else {
		   	writer = new BufferedWriter(new FileWriter(new File(directoryPath + "\"" + name)));
		}
	    
		for (String line : outputArea.getText().split("\\n")) {
	    	writer.write(line + "\n");
		} 
	     
	    writer.close();
	}

}
