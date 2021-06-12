package com.gogrocery.firebase;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.media.Ringtone;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Build;
import android.util.Log;

import androidx.core.app.NotificationCompat;
import androidx.work.OneTimeWorkRequest;
import androidx.work.WorkManager;

import com.gogrocery.Constants.SharedPreferenceManager;
import com.gogrocery.R;
import com.gogrocery.view.LoginActivity;
import com.gogrocery.view.MainActivityNew;
import com.gogrocery.view.MyOrdersDetailPage;
import com.gogrocery.view.SplashActivity;
import com.gogrocery.view.SubstituteActivity;
import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;

import java.util.Map;

public class MyFirebaseMessagingService extends FirebaseMessagingService {

    private static final String TAG = MyFirebaseMessagingService.class.getSimpleName();
    private SharedPreferenceManager mSharedPreferenceManager;

    int count = 0;

    @Override
    public void onCreate() {
        super.onCreate();
        mSharedPreferenceManager = new SharedPreferenceManager(getApplicationContext());
    }

    @Override
    public void onMessageReceived(RemoteMessage remoteMessage) {
        Log.d(TAG, "From: " + remoteMessage.getFrom());

        // Check if message contains a notification payload.
        if (remoteMessage.getNotification() != null) {
            Log.e(TAG, "Notification Body: " + remoteMessage.getNotification().getBody());
            //handleNotification(remoteMessage.getNotification().getBody());
        }


        // log the getting message from firebase
        Log.d(TAG, "From: " + remoteMessage.getFrom());
        //  if remote message contains a data payload.
        if (remoteMessage.getData().size() > 0) {
            Log.e(TAG, "Message data payload: " + remoteMessage.getData());
            Map<String, String> data = remoteMessage.getData();
            String jobType = data.get("type");
     /* Check the message contains data If needs to be processed by long running job
         so check if data needs to be processed by long running job */
            if (false) {
                // For long-running tasks (10 seconds or more) use WorkManager.
                scheduleLongRunningJob();
            } else {
                // Handle message within 10 seconds
                handleNow(data);
                try {


                    Uri notification = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
                    Ringtone r = RingtoneManager.getRingtone(getApplicationContext(), notification);
                    r.play();
//
                } catch (Exception e) {
                    e.printStackTrace();
                }

            }
        }

        // Check if message contains a data payload.
/*       if (remoteMessage.getData().size() > 0) {
        //if (remoteMessage.getNotification()!=null) {

            Log.d(TAG, "Data Payload: " + remoteMessage.getData().toString());
            try {


                Uri notification = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
                Ringtone r = RingtoneManager.getRingtone(getApplicationContext(), notification);
                r.play();
//
            } catch (Exception e) {
                e.printStackTrace();
            }

            try {
                JSONObject json = new JSONObject(remoteMessage.getData().toString());
                //Log.d(TAG, "onMessageReceived: " + json.toString());
                handleDataMessage(json);
            } catch (Exception e) {
                Log.d(TAG, "Exception: " + e.getMessage());
            }
        }*/
    }

    /* private void handleDataMessage(JSONObject json) {
         //NotificationUtils notificationUtils = new NotificationUtils(getApplicationContext());

         //Log.e(TAG, "push json: " + json.toString());

         try {
             //  JSONObject jsonObject = new JSONObject(tfun);
             JSONObject data = json.getJSONObject("result");
             Log.d(TAG, "handleDataMessage: " + data);

             if (!NotificationUtils.isAppIsInBackground(getApplicationContext())) {
                 // app is in foreground, broadcast the push message
                 Intent pushNotification = new Intent(AppConstants.PUSH_NOTIFICATION);
                 pushNotification.putExtra("message", data.getString("message"));
                 pushNotification.putExtra("title", data.getString("title"));
                 LocalBroadcastManager.getInstance(this).sendBroadcast(pushNotification);

                 try {
                     Uri notification = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
                     Ringtone r = RingtoneManager.getRingtone(getApplicationContext(), notification);
                     r.play();
                 } catch (Exception e) {
                     e.printStackTrace();
                 }
             } else {

                 try {
                     Uri notification = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
                     Ringtone r = RingtoneManager.getRingtone(getApplicationContext(), notification);
                     r.play();
                 } catch (Exception e) {
                     e.printStackTrace();
                 }

                 if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                     MyNotificationManager.getInstance(getApplicationContext())
                             .showNotificationMessage(data.getString("title"), data.getString("message"));
                 } else {
                     NotificationHandler notificationHandler = new NotificationHandler(getApplicationContext());
                     notificationHandler.showNotificationMessage(data.getString("title"), data.getString("message"));
                 }
             }
         } catch (JSONException e) {
             Log.e(TAG, "Json Exception: " + e.getMessage());
         } catch (Exception e) {
             Log.e(TAG, "Exception: " + e.getMessage());
         }
     }*/
    private void handleNow(Map<String, String> data) {
        if (data.containsKey("title") && data.containsKey("message")) {
            sendNotification(data.get("title"), data.get("message"),data.get("order_id"),data.get("noti_type"));
        }
    }
    private void scheduleLongRunningJob() {
        OneTimeWorkRequest work = new OneTimeWorkRequest.Builder(MyWorker.class)
                .build();
        WorkManager.getInstance().beginWith(work).enqueue();
    }
    private void sendNotification(String title, String messageBody,String order_id,String notificationType) {
        Intent intent;
        if(notificationType.equals("Order Substitute")){
            if(mSharedPreferenceManager.isLoggedIn()){
                intent = new Intent(this, SubstituteActivity.class);
            }else {
                intent = new Intent(this, LoginActivity.class);
            }
            intent.putExtra("pushOrderID",order_id);
            intent.putExtra("from_where", "pushNotification");
            intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
            PendingIntent pendingIntent = PendingIntent.getActivity(this, 0 /* Request code */, intent,
                    PendingIntent.FLAG_ONE_SHOT);
            String channelId = getString(R.string.default_notification_channel_id);
            Uri defaultSoundUri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
            NotificationCompat.Builder notificationBuilder =
                    new NotificationCompat.Builder(this, channelId)
                            .setSmallIcon(R.drawable.gogrocery_new_logo)
                            .setContentTitle(title)
                            .setContentText(messageBody)
                            .setAutoCancel(true)
                            .setSound(defaultSoundUri)
                            .setContentIntent(pendingIntent);
            NotificationManager notificationManager =
                    (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
            // Since android Oreo notification channel is needed.
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                // Channel human readable title
                NotificationChannel channel = new NotificationChannel(channelId,
                        "Cloud Messaging Service",
                        NotificationManager.IMPORTANCE_DEFAULT);
                notificationManager.createNotificationChannel(channel);
            }
            notificationManager.notify(0 /* ID of notification */, notificationBuilder.build());
        }else if(notificationType.equals("Order Picked")||notificationType.equalsIgnoreCase("Order delivery time updated")){
            if(mSharedPreferenceManager.isLoggedIn()){
                intent = new Intent(this, MyOrdersDetailPage.class);
            }else {
                intent = new Intent(this, LoginActivity.class);
            }
            intent.putExtra("orders_id",order_id);
            intent.putExtra("from_where", "pushNotification");
            intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
            PendingIntent pendingIntent = PendingIntent.getActivity(this, 0 /* Request code */, intent,
                    PendingIntent.FLAG_ONE_SHOT);
            String channelId = getString(R.string.default_notification_channel_id);
            Uri defaultSoundUri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
            NotificationCompat.Builder notificationBuilder =
                    new NotificationCompat.Builder(this, channelId)
                            .setSmallIcon(R.drawable.gogrocery_new_logo)
                            .setContentTitle(title)
                            .setContentText(messageBody)
                            .setAutoCancel(true)
                            .setSound(defaultSoundUri)
                            .setContentIntent(pendingIntent);
            NotificationManager notificationManager =
                    (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
            // Since android Oreo notification channel is needed.
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                // Channel human readable title
                NotificationChannel channel = new NotificationChannel(channelId,
                        "Cloud Messaging Service",
                        NotificationManager.IMPORTANCE_DEFAULT);
                notificationManager.createNotificationChannel(channel);
            }
            notificationManager.notify(0 /* ID of notification */, notificationBuilder.build());



        }else if(notificationType.equals("Place Order")) {
            if(mSharedPreferenceManager.isLoggedIn()){
                intent = new Intent(this, MyOrdersDetailPage.class);
            }else {
                intent = new Intent(this, LoginActivity.class);
            }
            intent.putExtra("orders_id",order_id);
            intent.putExtra("from_where", "pushNotification");
            intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
            PendingIntent pendingIntent = PendingIntent.getActivity(this, 0 /* Request code */, intent,
                    PendingIntent.FLAG_ONE_SHOT);
            String channelId = getString(R.string.default_notification_channel_id);
            Uri defaultSoundUri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
            NotificationCompat.Builder notificationBuilder =
                    new NotificationCompat.Builder(this, channelId)
                            .setSmallIcon(R.drawable.gogrocery_new_logo)
                            .setContentTitle(title)
                            .setContentText(messageBody)
                            .setAutoCancel(true)
                            .setSound(defaultSoundUri)
                            .setContentIntent(pendingIntent);
            NotificationManager notificationManager =
                    (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
            // Since android Oreo notification channel is needed.
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                // Channel human readable title
                NotificationChannel channel = new NotificationChannel(channelId,
                        "Cloud Messaging Service",
                        NotificationManager.IMPORTANCE_DEFAULT);
                notificationManager.createNotificationChannel(channel);
            }
            notificationManager.notify(0 /* ID of notification */, notificationBuilder.build());


        }else {
            Intent intent1 = new Intent(this, MainActivityNew.class);
            intent1.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
            PendingIntent pendingIntent = PendingIntent.getActivity(this, 0 /* Request code */, intent1,
                    PendingIntent.FLAG_ONE_SHOT);
            String channelId = getString(R.string.default_notification_channel_id);
            Uri defaultSoundUri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
            NotificationCompat.Builder notificationBuilder =
                    new NotificationCompat.Builder(this, channelId)
                            .setSmallIcon(R.drawable.gogrocery_new_logo)
                            .setContentTitle(title)
                            .setContentText(messageBody)
                            .setAutoCancel(true)
                            .setSound(defaultSoundUri)
                            .setContentIntent(pendingIntent);
            NotificationManager notificationManager =
                    (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
            // Since android Oreo notification channel is needed.
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                // Channel human readable title
                NotificationChannel channel = new NotificationChannel(channelId,
                        "Cloud Messaging Service",
                        NotificationManager.IMPORTANCE_DEFAULT);
                notificationManager.createNotificationChannel(channel);
            }
            notificationManager.notify(0 /* ID of notification */, notificationBuilder.build());
        }



    }
    @Override
    public void onNewToken(String token) {
        Log.d(TAG, "Refreshed token: " + token);

        mSharedPreferenceManager.saveDevKey(token);

    }
}
