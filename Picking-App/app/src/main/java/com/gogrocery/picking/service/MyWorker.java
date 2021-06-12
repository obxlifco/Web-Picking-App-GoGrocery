package com.gogrocery.picking.service;

import android.content.Context;
import android.util.Log;

import androidx.annotation.NonNull;

import javax.xml.transform.Result;
import androidx.work.Worker;
import androidx.work.WorkerParameters;
import io.reactivex.Scheduler;


public class MyWorker extends Worker {

    private static final String TAG = "MyWorker";

    public MyWorker(@NonNull Context appContext, @NonNull WorkerParameters workerParams) {
        super(appContext, workerParams);
    }

    @NonNull
    @Override
    public Result doWork() {
        Log.d(TAG, "Performing long running task in scheduled job");
        // TODO(developer): add long running task here.
        return Result.success();
    }
}
