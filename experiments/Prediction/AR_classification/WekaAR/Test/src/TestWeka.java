import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;

import java.io.File;

public class TestWeka {
    public static void main(String[] args) throws Exception {
        String dataDir = System.getProperty("user.dir") + "/Test/Data/";
        String csvFileName = "sample_1_ar.csv";
//        String arffFileName = "weather.numeric.arff";
        System.out.println("Data dir:" + dataDir + csvFileName);
        DataSource source = new DataSource(dataDir + csvFileName);
        Instances data = source.getDataSet();
        System.out.println(data.firstInstance());
        System.out.println("Load data successful!");



    }
}
