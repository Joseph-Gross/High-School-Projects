import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;

import javax.swing.JTextArea;

public class test {

	static JTextArea outputArea;
	
	public static void main(String[] args) {
		String directoryPath = "/Users/josephgross/Desktop/";
		createTextArea();
		
		ArrayList<String> candidates = new ArrayList<String>();
		candidates.add("A");
		candidates.add("B");
		candidates.add("C");
		candidates.add("D");
		candidates.add("E");
		
		outputArea.append("10000000 \n");
		
		for(int i=0; i<10000000; i++) {
			
			if(i%5!=0) {
				Collections.shuffle(candidates);
			}
			for(String element: candidates) {
				outputArea.append(element + " ");
			}
			System.out.println(i);
			outputArea.append("\n");
		}
	
		try {
			saveToFile(directoryPath, "random-test-data", true);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}
	
	public static void createTextArea() {
		outputArea = new JTextArea(30, 42);
		outputArea.setEditable(false);
		outputArea.setText("");
	}
	
	public static void saveToFile(String directoryPath, String name, Boolean apple) throws IOException {
		
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
