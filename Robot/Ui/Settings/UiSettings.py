# FIXME is this obsolete ?

class UiSettings:
    _preferences = dict()

    def __init____(self):

        pass

    def get_key_value(self, key):

        return

    def get_int_value(key):

        value = 0

        if key in UiSettings._preferences:
            value = UiSettings._preferences[key]

        if type(value) is not int:
            value = 0

        return value


"""package de.hska.lat.robot.ui.settings;

import java.util.Properties;


public class UiSettings 
{

	protected static Properties preferences;	
	
	
	
public static void setPreferences(Properties preferences)
{
	UiSettings.preferences=preferences;
	
	
	preferences.list(System.out);

}
	



public static void saveString(String key, String value)
{
	preferences.setProperty(key,value);
}	
	


public static void saveInt(String key, int value)
{
		preferences.setProperty(key, String.valueOf(value));
}







public static void saveBoolean(String key, boolean value)
{
		preferences.setProperty(key, String.valueOf(value));
}



/**
 * recover an Integer value from preferences. if there is no value for given Key it will returns default value 
 * @param key 
 * @param value default value for this key  
 * @return recovered value or default value if there is no key or key value is not numeric 
 */

public static int recoverInt(String key, int value)
{
	String valueAsString;	
	int keyValue;
	valueAsString=preferences.getProperty(key);

	try
	{
		keyValue=Integer.parseInt(valueAsString);
	}
	catch (Exception e)
	{
		keyValue= value;
	}


return(keyValue);

}



/**
 * recover an string value for given key, if this key do not exists return default value
 * @param key settings key
 * @param value default value for this key
 * @return recovered value or default
 */
public static String recoverString(String key, String value)
{
	String valueAsString;
	
	valueAsString=preferences.getProperty(key);
	if (valueAsString==null)
		valueAsString = value;
	
	return(valueAsString);
}



/**
 * recover an boolean value for given key, if this key do not exists return default value
 * @param key settings key
 * @param value default value for this key
 * @return recovered value or default
 */
public static boolean recoverBoolean(String key,boolean value)
{
	String valueAsString;	
	boolean keyValue;
	valueAsString=preferences.getProperty(key);

	try
	{
		keyValue=Boolean.parseBoolean(valueAsString);
	}
	catch (Exception e)
	{
		keyValue= value;
	}

	
	return(keyValue);
}





}
"""
