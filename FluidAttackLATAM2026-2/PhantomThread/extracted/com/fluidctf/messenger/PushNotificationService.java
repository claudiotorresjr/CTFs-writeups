package com.fluidctf.messenger;

import android.util.Log;
import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;

public class PushNotificationService extends FirebaseMessagingService {
    private static final String TAG = "FluidMsg";

    @Override
    public void onMessageReceived(RemoteMessage remoteMessage) {
        Log.d(TAG, "Push notification received from: " + remoteMessage.getFrom());

        if (remoteMessage.getNotification() != null) {
            String title = remoteMessage.getNotification().getTitle();
            String body = remoteMessage.getNotification().getBody();
            NotificationHelper.showNotification(this, title, body);
        }
    }

    @Override
    public void onNewToken(String token) {
        Log.d(TAG, "FCM token refreshed");
        TokenManager.getInstance().updateServerToken(token);
    }
}
