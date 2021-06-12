package com.gogrocery.DatabaseHandler;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.CursorIndexOutOfBoundsException;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import com.gogrocery.Models.ProductQuantityLocal;


import java.util.ArrayList;
import java.util.List;


public class DatabaseHandler extends SQLiteOpenHelper {
    private static final int DATABASE_VERSION = 1;
    private static final String DATABASE_NAME = "GoGrocery";
    private static final String TABLE_NAME = "ProductQty";
    private static final String KEY_ID = "id";
    private static final String KEY_PRODUCT_ID = "product_id";
    private static final String KEY_PRODUCT_QTY = "product_qty";

    private static final String TABLE_NAME_WISHLIST = "Wishlist";
    private static final String KEY_WISHLIST_ID = "id";
    private static final String KEY_WISHLIST_PRODUCT_ID = "wishlist_product_id";

    public DatabaseHandler(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
        //3rd argument to be passed is CursorFactory instance  
    }

    // Creating Tables  
    @Override
    public void onCreate(SQLiteDatabase db) {
        String CREATE_PRODUCT_QTY_TABLE = "CREATE TABLE " + TABLE_NAME + "("
                + KEY_ID + " INTEGER PRIMARY KEY,"
                + KEY_PRODUCT_ID + " TEXT,"
                + KEY_PRODUCT_QTY + " TEXT" + ")";
        db.execSQL(CREATE_PRODUCT_QTY_TABLE);
        String CREATE_PRODUCT_WISHLIST_TABLE = "CREATE TABLE " + TABLE_NAME_WISHLIST + "("
                + KEY_WISHLIST_ID + " INTEGER PRIMARY KEY,"
                + KEY_WISHLIST_PRODUCT_ID + " TEXT" + ")";
        db.execSQL(CREATE_PRODUCT_WISHLIST_TABLE);

    }

    // Upgrading database  
    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        // Drop older table if existed

        db.execSQL("DROP TABLE IF EXISTS " + TABLE_NAME);
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_NAME_WISHLIST);

        // Create tables again  
        onCreate(db);
    }

    // code to add the new DbModelCalendar
    public void addProductQty(ProductQuantityLocal argProductQuantityLocal) {
        SQLiteDatabase db = this.getWritableDatabase();

        ContentValues values = new ContentValues();
        values.put(KEY_PRODUCT_ID, argProductQuantityLocal.getProductId());
        values.put(KEY_PRODUCT_QTY, argProductQuantityLocal.getProductQty());

        // Inserting Row  
        db.insert(TABLE_NAME, null, values);
        //2nd argument is String containing nullColumnHack  
        db.close(); // Closing database connection  
    }
    public void addWishlistData(String argWishlistproductid) {
        SQLiteDatabase db = this.getWritableDatabase();

        ContentValues values = new ContentValues();
        values.put(KEY_WISHLIST_PRODUCT_ID, argWishlistproductid);

        // Inserting Row
        db.insert(TABLE_NAME_WISHLIST, null, values);
        //2nd argument is String containing nullColumnHack
        db.close(); // Closing database connection
    }


    public ProductQuantityLocal getSingleValueByProductId(String argDate) {
        SQLiteDatabase db = this.getReadableDatabase();
        ProductQuantityLocal mProductQuantityLocal = null;

        try {
            Cursor cursor = db.query(TABLE_NAME, new String[]{KEY_ID,
                            KEY_PRODUCT_ID, KEY_PRODUCT_QTY}, KEY_PRODUCT_ID + "=?",
                    new String[]{argDate}, null, null, null, null);
            if (cursor != null)
                cursor.moveToFirst();

            System.out.println("Rahul : getSingleValueByDate : 1 : " + cursor.getString(1));
            System.out.println("Rahul : getSingleValueByDate : 2 : " + cursor.getString(2));

            mProductQuantityLocal = new ProductQuantityLocal(cursor.getString(1),
                    cursor.getString(2));
        } catch (CursorIndexOutOfBoundsException mException) {
            System.out.println("Rahul : getSingleValueByDate : mException : " + mException.getMessage());
            return mProductQuantityLocal;
        }
        // return contact
        db.close();
        return mProductQuantityLocal;
    }

    public String checkAndSendProductQtyById(String argProductId) {
        SQLiteDatabase db = this.getReadableDatabase();
        String qty = "";
        try {
            Cursor cursor = db.query(TABLE_NAME, new String[]{KEY_ID,
                            KEY_PRODUCT_ID, KEY_PRODUCT_QTY}, KEY_PRODUCT_ID + "=?",
                    new String[]{argProductId}, null, null, null, null);
            if (cursor != null)
                cursor.moveToFirst();

            System.out.println("Rahul : getSingleValueByDate : 1 : " + cursor.getString(1));
            System.out.println("Rahul : getSingleValueByDate : 2 : " + cursor.getString(2));

            qty = cursor.getString(2);

        } catch (CursorIndexOutOfBoundsException mException) {
            System.out.println("Rahul : getSingleValueByDate : mException : " + mException.getMessage());
            return "0";
        }
        // return contact
        db.close();
        return qty;
    }

    public int returnQuantity(String argProductId) {
        SQLiteDatabase db = this.getReadableDatabase();
        int qty = 0;
        String Query = "Select " + KEY_PRODUCT_QTY + " from " + TABLE_NAME + " where " + KEY_PRODUCT_ID + " = " + argProductId;
        Cursor cursor = db.rawQuery(Query, null);

        cursor.close();
        return Integer.parseInt(cursor.getString(0));
    }

    public boolean CheckIsDataAlreadyInDBorNot(String argProductId) {
        SQLiteDatabase db = this.getReadableDatabase();
        String Query = "Select * from " + TABLE_NAME + " where " + KEY_PRODUCT_ID + " = " + argProductId;
        Cursor cursor = db.rawQuery(Query, null);
        if (cursor.getCount() <= 0) {
            cursor.close();
            return false;
        }
        cursor.close();
        return true;
    }

    // code to get the single  ----------------------------------------------------------

    public boolean checkWishlistAvailable(String argProductId) {
        SQLiteDatabase db = this.getReadableDatabase();
        String Query = "Select * from " + TABLE_NAME_WISHLIST + " where " + KEY_WISHLIST_PRODUCT_ID + " = " + argProductId;
        Cursor cursor = db.rawQuery(Query, null);
        if (cursor.getCount() <= 0) {
            cursor.close();
            return false;
        }
        cursor.close();
        return true;
    }
    // code to get all DbModelCalendar in a list view
    public List<ProductQuantityLocal> getAllProductQtyData() {
        List<ProductQuantityLocal> mDbModelCalendarList = new ArrayList<ProductQuantityLocal>();
        // Select All Query  
        String selectQuery = "SELECT  * FROM " + TABLE_NAME;

        SQLiteDatabase db = this.getWritableDatabase();
        Cursor cursor = db.rawQuery(selectQuery, null);

        // looping through all rows and adding to list  
        if (cursor.moveToFirst()) {
            do {
                ProductQuantityLocal mDbModelCalendar = new ProductQuantityLocal();

                mDbModelCalendar.setProductId(cursor.getString(1));
                mDbModelCalendar.setProductQty(cursor.getString(2));

                // Adding DbModelCalendar to list
                mDbModelCalendarList.add(mDbModelCalendar);
            } while (cursor.moveToNext());
        }

        // return mDbModelCalendarList
        return mDbModelCalendarList;
    }


    public int getWishlistData() {
        List<String> mDbModelCalendarList = new ArrayList<String>();
        // Select All Query
        String selectQuery = "SELECT  * FROM " + TABLE_NAME_WISHLIST;

        SQLiteDatabase db = this.getWritableDatabase();
        Cursor cursor = db.rawQuery(selectQuery, null);

        // return mDbModelCalendarList
        return cursor.getCount();
    }
    public int getWishlistColumnData() {
        List<String> mDbModelCalendarList = new ArrayList<String>();
        // Select All Query
        String selectQuery = "SELECT  * FROM " + TABLE_NAME_WISHLIST;

        SQLiteDatabase db = this.getWritableDatabase();
        Cursor cursor = db.rawQuery(selectQuery, null);

        // return mDbModelCalendarList
        return cursor.getColumnCount();

    }
    public String[] getWishlistColumnNameData() {
        List<String> mDbModelCalendarList = new ArrayList<String>();
        // Select All Query
        String selectQuery = "SELECT  * FROM " + TABLE_NAME_WISHLIST;

        SQLiteDatabase db = this.getWritableDatabase();
        Cursor cursor = db.rawQuery(selectQuery, null);

        // return mDbModelCalendarList
        return cursor.getColumnNames();

    }
  /*  public List<DbModelCalendar> getAllDbModelCalendarCount(String argDate) {
        List<DbModelCalendar> mDbModelCalendarList = new ArrayList<DbModelCalendar>();
        // Select All Query
        String selectQuery = "SELECT  * FROM " + TABLE_NAME_CALENDAR + " WHERE " + KEY_DATES + " = '" + argDate + "'";
        System.out.println("Rahul: selectQuery : " + selectQuery);
        SQLiteDatabase db = this.getWritableDatabase();
        Cursor cursor = db.rawQuery(selectQuery, null);

        // looping through all rows and adding to list
        if (cursor.moveToFirst()) {
            do {
                DbModelCalendar mDbModelCalendar = new DbModelCalendar();

                mDbModelCalendar.setDates(cursor.getString(1));
                mDbModelCalendar.setTime(cursor.getString(2));
                mDbModelCalendar.setBookingId(cursor.getString(3));
                mDbModelCalendar.setCarName(cursor.getString(4));
                mDbModelCalendar.setDatesEventCount(cursor.getString(5));


                // Adding DbModelCalendar to list
                mDbModelCalendarList.add(mDbModelCalendar);
            } while (cursor.moveToNext());
        }
        System.out.println("Rahul: selectQuery : mDbModelCalendarList : " + mDbModelCalendarList.size());
        // return mDbModelCalendarList
        return mDbModelCalendarList;
    }*/


    // code to update the single contact  --------------------------------------------Original
/*    public int updateByDate(DbModelCalendar argDbModelCalendar) {
        SQLiteDatabase db = this.getWritableDatabase();  
  
        ContentValues values = new ContentValues();  
        values.put(KEY_DATES, argDbModelCalendar.getDates());
        values.put(KEY_BOOKINGID, argDbModelCalendar.getBookingId());
        values.put(KEY_CAR_NAME,argDbModelCalendar.getCarName());
        values.put(KEY_DATES_EVENT_COUNT, argDbModelCalendar.getDatesEventCount());

        // updating row  
        return db.update(TABLE_NAME_CALENDAR, values, KEY_ID + " = ?",
                new String[] { String.valueOf(contact.getID()) });  
    }*/

    public int updateProductQuantityById(ProductQuantityLocal argProductQuantityLocal) {
        SQLiteDatabase db = this.getWritableDatabase();

        ContentValues values = new ContentValues();
        // values.put(KEY_DATES, argDbModelCalendar.getDates());
        values.put(KEY_PRODUCT_ID, argProductQuantityLocal.getProductId());
        values.put(KEY_PRODUCT_QTY, argProductQuantityLocal.getProductQty());

        // updating row
        return db.update(TABLE_NAME, values, KEY_PRODUCT_ID + " = ?",
                new String[]{argProductQuantityLocal.getProductId()});
    }

    public int updateBookingIdByDate(ProductQuantityLocal argProductQuantityLocal) {
        SQLiteDatabase db = this.getWritableDatabase();

        ContentValues values = new ContentValues();
        values.put(KEY_PRODUCT_QTY, argProductQuantityLocal.getProductQty());

        //  values.put(KEY_DATES, argDbModelCalendar.getDates());
      /*  values.put(KEY_BOOKINGID, argDbModelCalendar.getBookingId());
        values.put(KEY_CAR_NAME,argDbModelCalendar.getCarName());
        values.put(KEY_DATES_EVENT_COUNT, argDbModelCalendar.getDatesEventCount());
*/
        // updating row
        return db.update(TABLE_NAME, values, KEY_PRODUCT_ID + " = ?",
                new String[]{argProductQuantityLocal.getProductId()});
    }
/*
    public int updateCarNameByDate(DbModelCalendar argDbModelCalendar) {
        SQLiteDatabase db = this.getWritableDatabase();

        ContentValues values = new ContentValues();
        values.put(KEY_CAR_NAME, argDbModelCalendar.getCarName());
        //  values.put(KEY_DATES, argDbModelCalendar.getDates());
      *//*  values.put(KEY_BOOKINGID, argDbModelCalendar.getBookingId());
        values.put(KEY_CAR_NAME,argDbModelCalendar.getCarName());
        values.put(KEY_DATES_EVENT_COUNT, argDbModelCalendar.getDatesEventCount());
*//*
        // updating row
        return db.update(TABLE_NAME_CALENDAR, values, KEY_DATES + " = ?",
                new String[]{argDbModelCalendar.getDates()});
    }*/


    // Deleting single contact  
   /* public void deleteContact(Contact contact) {
        SQLiteDatabase db = this.getWritableDatabase();  
        db.delete(TABLE_CONTACTS, KEY_ID + " = ?",  
                new String[] { String.valueOf(contact.getID()) });  
        db.close();  
    }  */

    public void deleteSingleRecord(String argProductId) {
        SQLiteDatabase db = this.getWritableDatabase();
        db.delete(TABLE_NAME, KEY_PRODUCT_ID + " = ?",
                new String[]{String.valueOf(argProductId)});
        db.close();
    }

    public void deleteWishlistSingleRecord(String argProductId) {
        SQLiteDatabase db = this.getWritableDatabase();
        db.delete(TABLE_NAME_WISHLIST, KEY_WISHLIST_PRODUCT_ID + " = ?",
                new String[]{String.valueOf(argProductId)});
        db.close();
    }

    public void deleteAllRecord() {
        SQLiteDatabase db = this.getWritableDatabase();
        db.execSQL("delete from " + TABLE_NAME);
        db.close();
    }

    public void deleteAllRecordWishlist() {
        SQLiteDatabase db = this.getWritableDatabase();
        db.execSQL("delete from " + TABLE_NAME_WISHLIST);
        db.close();
    }


    // Getting contacts Count  
   /* public int getContactsCount() {
        String countQuery = "SELECT  * FROM " + TABLE_CONTACTS;  
        SQLiteDatabase db = this.getReadableDatabase();  
        Cursor cursor = db.rawQuery(countQuery, null);  
        cursor.close();  
  
        // return count  
        return cursor.getCount();  
    }  */

}  