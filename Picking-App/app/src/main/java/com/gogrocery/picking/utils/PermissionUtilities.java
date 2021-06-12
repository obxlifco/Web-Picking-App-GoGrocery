package com.gogrocery.picking.utils;

import android.app.Activity;
import android.view.View;

import com.karumi.dexter.Dexter;
import com.karumi.dexter.listener.multi.MultiplePermissionsListener;
import com.karumi.dexter.listener.single.PermissionListener;

/**
 * Created by Pratim on 4/12/17.
 */

public class PermissionUtilities {
    public static void singlePermission(Activity mActivity, String mPerimission, PermissionListener listener)
    {
        Dexter.withActivity(mActivity)
                .withPermission(mPerimission)
                .withListener(listener).check();
    }

    public static void multiplePermission(Activity mActivity, String[] mPerimissions,MultiplePermissionsListener listener)
    {
        Dexter.withActivity(mActivity)
                .withPermissions(mPerimissions)
                .withListener(listener).check();

    }
}
