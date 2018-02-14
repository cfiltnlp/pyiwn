import iitb.cfilt.cpost.newstemmer.StemmedToken;
import iitb.cfilt.cpost.newstemmer.Stemmer;
import iitb.cfilt.cpost.newstemmer.StemmerRuleResult;

import java.io.*;
import java.util.*;
import java.lang.reflect.Method;


/*
Compile and run this program from the current directory using the following command:

javac -cp ".:../lib/hindi_analyzer.jar" HindiMADemo.java
java -cp .:../lib/hindi_analyzer.jar HindiMADemo 
*/

public class HindiMADemo {

    private static Set<String> stopwords = new HashSet<>();

    private static final String RESOURCES_PATH = new File(System.getProperty("user.dir")).getParent() + "/resources/";

	public static void main(String[] args) throws Exception {
        String word = args[0];
        Stemmer stemmer = Stemmer.getInstance("hi", RESOURCES_PATH + "hindiConfig", RESOURCES_PATH);
        StemmedToken st = stemmer.stem(word);
        Vector<StemmerRuleResult> stems = st.getStemmedOutputs();
        
        System.out.println(stems);

        String root = stems.get(0).getRoot();
        System.out.println("Root: " + root);

        String paradigm = stems.get(0).getParadigm();

        String category = stems.get(0).getCategory();
        System.out.println("Category: " + category);

        LinkedList<String> suffixList = stems.get(0).getSuffixList();
        System.out.println("Suffix List: " + suffixList);
    }
}