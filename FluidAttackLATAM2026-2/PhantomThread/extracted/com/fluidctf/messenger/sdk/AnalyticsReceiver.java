package com.fluidctf.messenger.sdk;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

public class AnalyticsReceiver extends BroadcastReceiver {
    private static final String TAG = "AnalyticsSDK";

    @Override
    public void onReceive(Context context, Intent intent) {
        String action = intent.getAction();
        if ("com.fluidctf.messenger.sdk.ANALYTICS_EVENT".equals(action)) {
            String eventName = intent.getStringExtra("event_name");
            if (eventName != null) {
                Log.d(TAG, "Received analytics event broadcast: " + eventName);
                AnalyticsTracker.getInstance().logEvent(eventName);
            }
        }
    }
}
