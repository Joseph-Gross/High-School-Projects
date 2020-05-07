import java.awt.Color;
import java.io.FileNotFoundException;

import javax.swing.*;

public class Main {
	
	public static void main(String[] args) throws FileNotFoundException {
		JPanel instructions = new InitialInput();
		
		JFrame frame = new JFrame();
		frame.setTitle("Dubard's Difficult Dilemma");
		frame.getContentPane().setBackground(new Color(221,160,221));
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setSize(385, 550);
		frame.add(instructions);
		frame.setResizable(false);
		frame.setVisible(true); 
	}
}
