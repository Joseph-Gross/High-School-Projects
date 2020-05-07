import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.nio.file.Files;
import java.util.ArrayList;

import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.filechooser.FileNameExtensionFilter;

public class OutputFrame extends JFrame{

	private JTextArea outputArea;
	private ArrayList<String> result;
	
	private JButton saveButton;
	private JFrame finalFrame;
	
	private JLabel saveLabel;
	private JTextField nameField;
	
	
	public OutputFrame(JTextArea inputArea, ArrayList<String> inputResult) {
		outputArea = inputArea;
		result = inputResult;
		saveLabel = new JLabel();
		
		finalFrame = new JFrame("Dubard's Difficult Dilemma");
		JPanel outputPanel = new JPanel();
		JLabel outputLabel = new JLabel("Optimized Pairings");
		
		createTextArea();
		JScrollPane scrollPane = new JScrollPane(outputArea);

		createSaveButton();
		createNameField();
		
		outputPanel.setBackground(new Color(221,160,221));
		outputPanel.add(outputLabel, BorderLayout.PAGE_START);
		outputPanel.add(scrollPane, BorderLayout.CENTER);
		outputPanel.add(saveButton);
		outputPanel.add(nameField);
		outputPanel.add(saveLabel);

		finalFrame.setTitle("Dubard's Difficult Dilemma");
		finalFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		finalFrame.setBounds(300, 150, 385, 550);
		finalFrame.add(outputPanel);
		finalFrame.setResizable(false);
		finalFrame.setVisible(true); 
	}
	
	public void createNameField() {
		final int fieldWidth = 10;
		
		nameField = new JTextField(fieldWidth);
		nameField.setText("");
	}
	
	public void createTextArea() {
		outputArea = new JTextArea(25, 25);
		outputArea.setEditable(false);
		outputArea.setText("");
		
		for(int i=0; i<result.size(); i++) {
			outputArea.append("Pair " + (i+1) + ": " + result.get(i) + "\n");
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

	public void saveToFile(String directoryPath, String name, Boolean apple) throws IOException {
		BufferedWriter writer;
		if(apple) {
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
