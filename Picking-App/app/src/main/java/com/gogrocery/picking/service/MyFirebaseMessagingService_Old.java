package com.gogrocery.picking.service;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Build;
import android.util.Log;

import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;
import com.gogrocery.picking.R;
import com.gogrocery.picking.activity.SplashActivity;
import com.gogrocery.picking.utils.AppUtilities;

import java.util.Map;

import androidx.annotation.NonNull;
import androidx.core.app.NotificationCompat;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

public class MyFirebaseMessagingService_Old extends FirebaseMessagingService {
    private NotificationHelper notificationHelper;
    private int noti_id=100;

    @Override
    public void onNewToken(@NonNull String token) {
        super.onNewToken(token);
        Log.e("TAG", "Refreshed token: " + token);
        Intent i=new Intent("com.nav155.gogrocerypicking.receiver.NEW_TOKEN");
        i.putExtra("token",token);
        sendBroadcast(i);

    }

    @Override
    public void onMessageReceived(@NonNull RemoteMessage remoteMessage) {
        super.onMessageReceived(remoteMessage);
        Log.d("TAG", "From: " + remoteMessage.getFrom());

        // Check if message contains a data payload.
        if (remoteMessage.getData().size() > 0) {
            Log.d("TAG", "Message data payload: " + remoteMessage.getData());

            if (/* Check if data needs to be processed by long running job */ true) {
                // For long-running tasks (10 seconds or more) use WorkManager.
                //scheduleJob();
            } else {
                // Handle message within 10 seconds
                //handleNow();
            }
            //Log.e("TAG", "Data Payload: " + remoteMessage.getData().toString());

            try {
                Map<String, String> data = remoteMessage.getData();
                //JSONObject json = new JSONObject(remoteMessage.getData().toString());
                handleDataMessage(data);
            } catch (Exception e) {
                Log.e("TAG", "Exception: " + e.getMessage());
            }

        }

        // Check if message contains a notification payload.
        if (remoteMessage.getNotification() != null) {
            Log.e("TAG", "Notification Body: " + remoteMessage.getNotification().getBody());
            handleNotification(remoteMessage.getNotification().getBody(), remoteMessage.getNotification().getTitle(),remoteMessage.getData().get("order_id"));
        }
    }

    private void handleNotification(String message, String title, String order_id) {
        if (!AppUtilities.isAppIsInBackground(getApplicationContext())) {
            // app is in foreground, broadcast the push message
            Intent pushNotification = new Intent("pushNotification");
            pushNotification.putExtra("message", message);
            LocalBroadcastManager.getInstance(this).sendBroadcast(pushNotification);
            //sendNotification(message,"Notification");
            notificationHelper = new NotificationHelper(getApplicationContext());
            notificationHelper.createNotification(title, message, order_id);
        } else {
            // If the app is in background, firebase itself handles the notification
            notificationHelper = new NotificationHelper(getApplicationContext());
            notificationHelper.createNotification(title, message, order_id);
        }
    }

    private void handleDataMessage(Map<String, String> data) {
        Log.e("TAG", "push json: " + data.toString());

        try {
            /*JSONObject data = json.getJSONObject("data");

            String title = data.getString("title");
            String message = data.getString("message");
            boolean isBackground = data.getBoolean("is_background");
            String imageUrl = data.getString("image");
            String timestamp = data.getString("timestamp");
            JSONObject payload = data.getJSONObject("payload");*/
            /* String nt_type= payload.getString("notification_type");
            String story_title=payload.getString("story_title");
            String user_name=payload.getString("user_name");
            String narrator_id="",narrator="",gender="";*/
            //JSONObject data = json.getJSONObject("data");
            //String title = data.getString("title");
            //String pushmsg = json.optString("order_id");

            /*Intent pushNotification = new Intent("pushNotification");
            pushNotification.putExtra("key", pushmsg);*/
            //LocalBroadcastManager.getInstance(this).sendBroadcast(pushNotification);
            sendNotification(data.get("title"), data.get("message"),data.get("order_id"));
        }catch (Exception e) {
            Log.e("TAG", "Exception: " + e.getMessage());
        }
    }

    /*private void sendNotification(String message, String title) {
        Intent intent = new Intent(this, SplashActivity.class);
        intent.putExtra("pushOrderID", message);
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        int requestCode = 0;
        PendingIntent pendingIntent = PendingIntent.getActivity(this, requestCode, intent, PendingIntent.FLAG_ONE_SHOT);
        Uri sound = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
        // final Uri alarmSound = Uri.parse(ContentResolver.SCHEME_ANDROID_RESOURCE
        //       + "://" + getApplicationContext().getPackageName() + "/raw/noty");
        NotificationCompat.Builder noBuilder = new NotificationCompat.Builder(this)
                .setSmallIcon(R.drawable.ic_notification)
                .setContentTitle(title)
                .setContentText(message)
                .setAutoCancel(true)
                .setContentIntent(pendingIntent);
        noBuilder.setSound(sound);
        NotificationManager notificationManager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
        notificationManager.notify(noti_id, noBuilder.build()); //0 = ID of notification
        noti_id++;
    }*/

    private void sendNotification(String title, String messageBody, String order_id) {
        Log.e("TAG", "sendNotification: " + order_id);
        Intent intent = new Intent(this, SplashActivity.class);
        intent.putExtra("pushOrderID",order_id);
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0 /* Request code */, intent,
                PendingIntent.FLAG_ONE_SHOT);
        String channelId = getString(R.string.default_notification_channel_id);
        Uri defaultSoundUri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
        NotificationCompat.Builder notificationBuilder =
                new NotificationCompat.Builder(this, channelId)
                        .setSmallIcon(R.drawable.ic_notification)
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
