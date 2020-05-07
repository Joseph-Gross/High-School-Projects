import java.util.ArrayList;

public class Student {
		String name;
		Boolean choiceSet;
		
		ArrayList<String> choiceList;
		String choice1;
		String choice2;
		String choice3;
		
		String[] choices;
		
		ArrayList<String> namesList;
		
	public Student(ArrayList<String> names, int index) {
		namesList = new ArrayList<String>(names);
		name = namesList.get(index);
		setChoiceList(new ArrayList<String>(namesList));
		choiceSet = false;
			
		choiceList.remove(name);
			
		choice1 = "none";
		choice2 = "none";
		choice3 = "none";
			
		//System.out.println(name + ": " + namesList );
	}
		
	public void setChoiceList(ArrayList<String> choice1List) {
		choice1List.add(0, "none");
		this.choiceList = choice1List;
	}
		
	public ArrayList<String> getChoiceList() {
		return choiceList;
	}
		
	public void setChoice1(String name) {
		choice1 = name;
	}
		
	public void setChoice2(String name) {
		choice2 = name;
	}
		
	public void setChoice3(String name) {
		choice3 = name;
	}
		
	public void setChoice() {
		choices = new String[4];
		choices[0] = name;
		choices[1] = choice1;
		choices[2] = choice2;
		choices[3] = choice3;
	}
		
	public String[] getStudentInfo() {
		return choices;
	}
	
	public void choiceSet() {
		choiceSet = true;
	}
}