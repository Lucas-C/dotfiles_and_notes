// echo -e 'Class-Path: .\nMain-Class: Cat' > MANIFEST.MF
// javac Cat.java
// jar cmf MANIFEST.MF cat.jar Cat.java
// java -jar cat.jar < Cat.java
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Cat {
    public static void main(String[] args) {
        InputStreamReader inReader = null;
        if (args.length == 1) {
            try {
                inReader = new FileReader(args[0]);
            } catch (FileNotFoundException ex) {
                System.out.println("File not found: " + args[0]);
            }
        } else {
            inReader = new InputStreamReader(System.in);
        }
        try {
            BufferedReader inBuffer = new BufferedReader(inReader);
            String line;
            while ((line = inBuffer.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException ex) {
            System.out.println("Input/output error.");
        }
    }
}
