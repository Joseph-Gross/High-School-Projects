import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.io.*;

public class DubardAlgorithm2 {
	
	private static int CLASS_SIZE;
	private static int NUMBER_OF_CHOICES = 3;
	
	private static int[][] input; 
	private static int[][] scores; 
	private static int[][] scoresFinal;  
	
	private static ArrayList<String> pairs = new ArrayList<String>();
	private static ArrayList<String> allGroups = new ArrayList<String>();
	private static ArrayList<validGroup> validGroups = new ArrayList<validGroup>();
	
	private static ArrayList<String> names =  new ArrayList<String>();
	private static ArrayList<String> correctGrouping = new ArrayList<String>();
		
	public DubardAlgorithm2(int[][] initialInput, ArrayList<String> namesInput) throws FileNotFoundException {	
		if(initialInput.length % 2 == 1) {
			input = modifiedInput(initialInput);
			namesInput.add("Alone");
		}else {
			input = initialInput;
		}
		names = namesInput;
		
		createInitial();
		fillScores();
		fillPairs();
		allSubsets(pairs, CLASS_SIZE);
		
		createvalidGroups();
		findMax();
	}
	

	public static void createvalidGroups(){
		for(int x = 0; x < allGroups.size(); x++){
			validGroups.add(new validGroup(allGroups.get(x)));
		}
		assignScores();

//		System.out.println("Valid Groups (" + allGroups.size() + "): ");
//		for(int i = 0; i < validGroups.size(); i++){
//			System.out.print("Score: " + validGroups.get(i).getScore() + " - ");
//			validGroups.get(i).outputPairs();
//		}
	}
	
	public static void assignScores(){
		for(int s = 0; s < validGroups.size(); s++){
			int counter = 0; 
			for(int x = 0; x < validGroups.get(s).getPairs().size(); x++){
				String current = validGroups.get(s).getPairs().get(x);
				int a1 = (int)current.charAt(0);
				int a2 = current.charAt(1);
				counter += scoresFinal[a1-65][a2-65];
			}
			validGroups.get(s).setScore(counter);
		}
	}

	public static void findMax(){
		int maxScore = 0; 
		for(int x = 0; x < validGroups.size(); x++){
			int s = validGroups.get(x).getScore();
			if(s > maxScore)
				maxScore = s;
		}
		
		//System.out.println("Best Group(s):");
		for(int x = 0; x < validGroups.size(); x++){
			if(validGroups.get(x).getScore() != maxScore) {
				validGroups.remove(x);
				x--;
			}
		}
		
		ArrayList<String> validPair = new ArrayList<String>();
		
		if(validGroups.size() > 1) {
			int random = (int) ((validGroups.size()-1) * Math.random());
			validPair = validGroups.get(random).getPairs();
			//validGroups.get(random).outputPairs();
		} else {
			validPair = validGroups.get(0).getPairs();
			//validGroups.get(0).outputPairs();
		}
		
		for(int i=0; i<validPair.size(); i++) {
			String pair = validPair.get(i);
			String letter1 = pair.substring(0, 1);
			String letter2 = pair.substring(1);
			String name1 = names.get(LetterToNum(letter1));
			String name2 = names.get(LetterToNum(letter2));
			
//			System.out.println(i + ": " + letter1 + " " + letter2 + " " + name1 + " " + name2);
			correctGrouping.add(name1 + ", " + name2);
		}
		
//		System.out.print(correctGrouping);
	}
	
	public static ArrayList<String> getCorrectGrouping() {
		return correctGrouping;
	}
	
	
	public static void createInitial() throws FileNotFoundException{
		CLASS_SIZE = input.length;
	
		
		//initial = new String[CLASS_SIZE][NUMBER_OF_CHOICES]; 
		scores = new int[CLASS_SIZE][CLASS_SIZE]; 
		scoresFinal = new int[CLASS_SIZE][CLASS_SIZE];  
		
//		System.out.println("# of people: " + CLASS_SIZE);
//		System.out.println("# of choices per person: " + NUMBER_OF_CHOICES);
	}
	
	public static void fillScores(){ //at end set all blanks to 0
		scores = input;
		
		displayArray(input);
	}
	
	public static void reflectScores() {
		//Reflects the matrix across diagonal and adds it
		for(int x = 0; x < scores.length; x++){
			for(int y = 0; y < scores[0].length; y++){
					scoresFinal[x][y] = scores[x][y] + scores[y][x];
			}
		}
		
		if(invalidData(scoresFinal)) {
			for(int i=0; i<scoresFinal.length; i++) {
				for(int j=0; j<scoresFinal[0].length; j++) {
					if(scoresFinal[i][j] > 0) {
						scoresFinal[i][j] *= 2;
					}
				}
			}
		}
		
		for(int[] row: scoresFinal) {
			if(isEmpty(row)) {
				fillRow(row);
			}
		}
		
		
		displayArray(scoresFinal);
	}
	
	//Sets one half of 2d Array equal to 0
	public static void cleanScores() {
		for(int x = 0; x < scores.length; x++){
			for(int y = 0; y < scores[0].length; y++){
					if(x < y) {
						scoresFinal[x][y] = 0;
					}
			}
		}
		//displayArray(scoresFinal);
	}

	public static void fillPairs() {
		reflectScores();
		cleanScores();
		for(int x = 0; x < scores.length; x++){
			for(int y = 0; y < scores[0].length; y++){
					if(scoresFinal[x][y] > 0) {
						pairs.add(numToLetter(x) + numToLetter(y));
						//System.out.println(x +"," +y);
					}
			}
		}
		reflectScores();
		pairs = sortArrayList(pairs);
		//System.out.println("# of Pairs (" + pairs.size() + "): " + pairs);
	}
	
	public static int[][] modifiedInput(int[][] arr) {
		int[][] output = new int[arr.length+1][arr[0].length+1];
		
		for(int i=0; i<output.length; i++) {
			for(int j=0; j<output[0].length; j++) {
				if(i<arr.length && j<arr[0].length) {
					output[i][j] = arr[i][j];
				} else {
					output[i][j] = 0;
				}
			}
		}
		
		return output;
	}
	
	
	public static String numToLetter(int number) {
		
		switch(number) {
		case 0: return "A";
		case 1: return "B";
		case 2: return "C";
		case 3: return "D";
		case 4: return "E";
		case 5: return "F";
		case 6: return "G";
		case 7: return "H";
		case 8: return "I";
		case 9: return "J";
		case 10: return "K";
		case 11: return "L";
		case 12: return "M";
		case 13: return "N";
		case 14: return "O";
		case 15: return "P";
		case 16: return "Q";
		case 17: return "R";
		case 18: return "S";
		case 19: return "T";
		case 20: return "U";
		case 21: return "V";
		case 22: return "W";
		case 23: return "X";
		case 24: return "Y";
		case 25: return "Z";
		default: return "";			
		}
	}
	
	public static int LetterToNum(String letter) {
		
		switch(letter) {
		case "A": return 0;
		case "B": return 1;
		case "C": return 2;
		case "D": return 3;
		case "E": return 4;
		case "F": return 5;
		case "G": return 6;
		case "H": return 7;
		case "I": return 8;
		case "J": return 9;
		case "K": return 10;
		case "L": return 11;
		case "M": return 12;
		case "N": return 13;
		case "O": return 14;
		case "P": return 15;
		case "Q": return 16;
		case "R": return 17;
		case "S": return 18;
		case "T": return 19;
		case "U": return 20;
		case "V": return 21;
		case "W": return 22;
		case "X": return 23;
		case "Y": return 24;
		case "Z": return 25;
		default: return 0;			
		}
	}
	
	public static void displayArray(int[][] array) {
		System.out.println();
		for(int x = 0; x < array.length; x++){
			for(int y = 0; y < array[0].length; y++){
					System.out.print(array[x][y] + "  ");
			}
			System.out.println();
		}
	}
	
	public static ArrayList<String> sortArrayList(ArrayList<String> list) {
		ArrayList<String> sortedList = new ArrayList<String>();
		
		for(String element : list) {
			sortedList.add(alphabeticalOrder(element));
		}
		list = sortedList;
		Collections.sort(list);
		return list;
	}
	
	public static String alphabeticalOrder(String line) {
		char[] charArray = line.toCharArray();
		Arrays.sort(charArray);
		return new String(charArray); 
	}
	
	
	
	public static ArrayList<String> allPairs(ArrayList<String> people) {
		ArrayList<String> allPairs = new ArrayList<String>();
		
		for(int i=0; i < people.size(); i++) {
			for(int j=i+1; j < people.size(); j++) {
				allPairs.add(people.get(i) + people.get(j));
			}
		}
		
		return allPairs;
	}
    
	public static void allSubsets(ArrayList<String> pairs, int length) {
		
		for(int i = 0; i< pairs.size();i++){ 
	          powerSet(allGroups, pairs, "", i, length);
	    }
		
//		System.out.print("Valid Groups (" + allGroups.size() + "): ");
//		System.out.println(allGroups);
	}
	
	public static void powerSet(ArrayList<String> allSubsets, ArrayList<String> string, String substring, int index, int length) {
		String subSet = string.get(index);
		subSet = substring + subSet;
		if(subSet.length() == length && isValid(subSet)) {
				allSubsets.add(subSet);
		} if(subSet.length() > length) {
			return;
		} else {
			for(int i=index+1; i < string.size(); i++) {
				powerSet(allSubsets, string, subSet, i, length);
			}
		}
	}
	
	public static Boolean isValid(String line) {
		String test = line;
		for(int i=0; i < line.length()-1; i++) {
			test = line.substring(i+1, line.length());
			if(test.contains(line.charAt(i) + "")) {
				return false;
			}
		}
		return true;
	}
	
	public static Boolean invalidData(int[][] data) {
		for(int[] row: data) {
			if(isEmpty(row)) {
				return true;
			}
		}
		
		return false;
	}
	
	
	public static Boolean isEmpty(int[] num) {
		for(int i: num) {
			if(i!=0) {
				return false;
			}
		}
		return true;
	}
	
	public static void fillRow(int[] num) {
		int random = 0;
		
		
		while(sum(num) < 3) {
			random = (int) (Math.random() * (num.length-1));
			
			if(num[random] == 0) {
				num[random]++;
			}
		}
	}

	public static int sum(int[] num) {
		int sum = 0;
		for(int a: num) {
			sum+=a;
		}
		
		return sum;
	}
	
	public static int choose(int a, int b) {
		int numerator = 1;
		for(int i=0; i<b; i++) {
			numerator *= a - i;
		}
		
		return numerator / factorial(b);
	}
	
	public static int factorial(int n) {
		if(n == 1) {
			return 1;
		} 
		else {
			return n * factorial(n-1);
		}
	}

}
