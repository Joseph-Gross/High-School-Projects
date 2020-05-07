import javax.swing.*;
import java.awt.*;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
public class StudentPanel implements ItemListener {

	public StudentTeacher student; 
	public JPanel panel;
	public JLabel nameLabel;
	private JComponent frame; 

	public JComboBox<String> firstChoiceList;
	public JComboBox<String> secondChoiceList; 
	public JComboBox<String> thirdChoiceList;
	
	public static int x = 50;
	public static int y = 50;
	
	public StudentPanel(StudentTeacher s){
		student = s;
		nameLabel = new JLabel(student.name);
		panel = new JPanel();
		firstChoiceList = new JComboBox(s.choice1List.toArray());
		secondChoiceList = new JComboBox(s.choice2List.toArray());
		thirdChoiceList = new JComboBox(s.choice3List.toArray());
		firstChoiceList.addItemListener(this);
		secondChoiceList.addItemListener(this);
		thirdChoiceList.addItemListener(this);
		
		initialize(x,y);
		y+=100;
	}
	
	public void initialize(int x, int y){
		panel.setBackground(SystemColor.textHighlight);
		panel.setBounds(x, y, 704, 98);
		panel.setLayout(null);
		
		nameLabel.setBounds(33, 31, 101, 41);
		panel.add(nameLabel);
		
		firstChoiceList.setBounds(144, 31, 160, 40);
		panel.add(firstChoiceList);
		
		secondChoiceList.setBounds(324, 31, 160, 40);
		panel.add(secondChoiceList);
		
		thirdChoiceList.setBounds(500, 31, 160, 40);
		panel.add(thirdChoiceList);
	}
	

	@Override
	public void itemStateChanged(ItemEvent event) {
		if(event.getSource().equals(firstChoiceList)){
		/*	
			if(firstChoiceList.getSelectedItem().equals("RESET LIST")){
				firstChoiceList = new JComboBox(student.choice1List.toArray());
				firstChoiceList.setBounds(154, 31, 160, 40);
				firstChoiceList.setSelectedIndex(0);
			}
			*/
			student.choice1 = (String) firstChoiceList.getSelectedItem(); 
			secondChoiceList.removeItem(student.choice1);
			thirdChoiceList.removeItem(student.choice1);
			
			
		}
		else if(event.getSource().equals(secondChoiceList)){
		/*	
			if(secondChoiceList.getSelectedItem().equals("RESET LIST")){
				secondChoiceList = new JComboBox(student.choice2List.toArray());
				secondChoiceList.setBounds(334, 31, 160, 40);
				secondChoiceList.setSelectedIndex(0);
			}
			*/
				student.choice2 = (String) secondChoiceList.getSelectedItem();
				firstChoiceList.removeItem(student.choice2);
				thirdChoiceList.removeItem(student.choice2);

			
			
		}
		else if(event.getSource().equals(thirdChoiceList)){
		/*
			if(thirdChoiceList.getSelectedItem().equals("RESET LIST")){
				thirdChoiceList = new JComboBox(student.choice3List.toArray());
				thirdChoiceList.setBounds(509, 31, 160, 40);
				thirdChoiceList.setSelectedIndex(0);
			}
			*/
			student.choice3 = (String) thirdChoiceList.getSelectedItem();
			firstChoiceList.removeItem(student.choice3);
			secondChoiceList.removeItem(student.choice3);
			
			
		}
	}


}