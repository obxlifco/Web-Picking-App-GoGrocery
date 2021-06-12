//
//  AppDelegate.swift
//  GoGrocery
//
//  Created by BMS-09-M on 16/12/19.
//  Copyright © 2019 BMS-09-M. All rights reserved.
//

import UIKit
import CoreData
import GooglePlaces
import GoogleMaps
import GoogleSignIn
import IQKeyboardManagerSwift
import Firebase
import FirebaseAnalytics
import FBSDKCoreKit
import SwiftyJSON
import Alamofire
import UserNotifications
@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {
    var window: UIWindow?
    
    let googleApiKey = "AIzaSyD0JWP3nYNYwPLtlRvkCCPw3AiyCadYbBk"
    //        let googleApiKey = "AIzaSyDdnHSfwdG3jfIIL7pPw1S36RM0tcXvwgo"
    
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        // Override point for customization after application launch.
        IQKeyboardManager.shared.enable = true
        GMSPlacesClient.provideAPIKey("\(googleApiKey)")
        GMSServices.provideAPIKey("\(googleApiKey)")
        GIDSignIn.sharedInstance().clientID = "330707394744-8ju6thmuuv05okgunqk7c4upgtv83n0e.apps.googleusercontent.com"
        Crashlytics.initialize()
        self.checkLocation()
        ApplicationDelegate.shared.application( application,didFinishLaunchingWithOptions: launchOptions )
        FirebaseApp.configure()
        Messaging.messaging().delegate = self
        
        //        if #available(iOS 10.0, *) {
        //            // For iOS 10 display notification (sent via APNS)
        //            UNUserNotificationCenter.current().delegate = self
        //
        //            let authOptions: UNAuthorizationOptions = [.alert, .badge, .sound]
        //            UNUserNotificationCenter.current().requestAuthorization(
        //                options: authOptions,
        //                completionHandler: {_, _ in })
        //        } else {
        //            let settings: UIUserNotificationSettings =
        //                UIUserNotificationSettings(types: [.alert, .badge, .sound], categories: nil)
        //            application.registerUserNotificationSettings(settings)
        //        }
        //        application.registerForRemoteNotifications()
        // Just Check for git
        
        if #available(iOS 10.0, *) {
            let authOptions: UNAuthorizationOptions = [.alert, .badge, .sound]
            UNUserNotificationCenter.current().requestAuthorization(
                options: authOptions,
                completionHandler: {_, _ in })
            
            // For iOS 10 display notification (sent via APNS)
            UNUserNotificationCenter.current().delegate = self
            
        } else {
            let settings: UIUserNotificationSettings =
                UIUserNotificationSettings(types: [.alert, .badge, .sound], categories: nil)
            application.registerUserNotificationSettings(settings)
        }
        application.registerForRemoteNotifications()
        return true
    }
    
    
    func setUpUpdateXibFunc () {
        requestAppUpdateGlobal()
        appUpdateTypeViewXib.btnUpgrade.addTarget(self, action: #selector(btnUpgradeClick), for: .touchUpInside)
        appUpdateTypeViewXib.btnUpgrade.layer.cornerRadius = 5
        appUpdateTypeViewXib.btnUpgrade.addShadow1()
        appUpdateTypeViewXib.imgImage.layer.cornerRadius = 5
        appUpdateTypeViewXib.imgImage.addShadow1()
        appUpdateTypeViewXib.updateView.layer.cornerRadius = 5
        appUpdateTypeViewXib.updateView.layer.shadowRadius = 1
        appUpdateTypeViewXib.updateView.layer.shadowColor = UIColor.gray.cgColor
        appUpdateTypeViewXib.updateView.layer.shadowOpacity = 0.4
        appUpdateTypeViewXib.updateView.layer.shadowOffset = CGSize(width: -1, height: 4)
    }
    
    @objc func btnUpgradeClick(sender: UIButton!) {
        // UIApplication.shared.openURL(NSURL(string: "https://qr.tapnscan.me/gogrocery")! as URL)
        UIApplication.shared.open(URL(string: "https://apps.apple.com/in/app/gogrocery/id1503352361")!, options: [:], completionHandler: nil)
    }
    
    func application( _ application: UIApplication,continue userActivity: NSUserActivity,restorationHandler: @escaping ([UIUserActivityRestoring]?) -> Void) -> Bool {
        guard userActivity.activityType == NSUserActivityTypeBrowsingWeb,
            let incomingURL = userActivity.webpageURL,
            let components = NSURLComponents(url: incomingURL, resolvingAgainstBaseURL: true),
            let path = components.path else {
                return false
                
        }
        // print(path)
        let pathAr = path.components(separatedBy: "/")
        guard pathAr.count > 0 else {
            return false
        }
        if pathAr.contains("reset-password") {
            let resetToken = pathAr[pathAr.count - 2]
            //           let mainStoryboardIpad : UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
            //            let initialViewControlleripad = mainStoryboardIpad.instantiateViewController(withIdentifier: "ResetPasswordViewController") as! ResetPasswordViewController
            //            initialViewControlleripad.resetTokenInReset = resetToken
            //           self.window = UIWindow(frame: UIScreen.main.bounds)
            //           self.window?.rootViewController = initialViewControlleripad
            //           self.window?.makeKeyAndVisible()
            
            let mainVC = UIStoryboard.init(name: "Main", bundle: nil).instantiateViewController(withIdentifier: "ResetPasswordViewController") as! ResetPasswordViewController
            let mainNav = UINavigationController.init(rootViewController: mainVC)
            mainVC.resetTokenInReset = resetToken
            appdelegate.window?.rootViewController = mainNav
            
        }
        else {
            if pathAr.contains("approved-order") {
                print("asdxasdxa")
                print(pathAr)
                let paymetToken = "\(pathAr[pathAr.count - 2])/?link=/"
                print(paymetToken)
                
                let mainStoryboardIpad : UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                let initialViewControlleripad = mainStoryboardIpad.instantiateViewController(withIdentifier: "OrderDetailsViewController") as! OrderDetailsViewController
                initialViewControlleripad.paymentTokenInReset = paymetToken
                initialViewControlleripad.pageFrom = "deepLink"
                
                let navigationController = UINavigationController(rootViewController: initialViewControlleripad)
                self.window = UIWindow(frame: UIScreen.main.bounds)
                self.window?.rootViewController = navigationController
                self.window?.makeKeyAndVisible()
            }
            else {
                let mainStoryboardIpad : UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
                let initialViewControlleripad = mainStoryboardIpad.instantiateViewController(withIdentifier: "MarkLocationViewController") as! MarkLocationViewController
                self.window = UIWindow(frame: UIScreen.main.bounds)
                self.window?.rootViewController = initialViewControlleripad
                self.window?.makeKeyAndVisible()
            }
        }
        return true
        
    }
    
    func applicationDidBecomeActive(_ application: UIApplication) {
        // AppEvents.activateApp()
    }
    func application(_ app: UIApplication, open url: URL, options: [UIApplication.OpenURLOptionsKey : Any] = [:]) -> Bool {
        print(url)
        return true
    }
    
    func applicationWillResignActive(_ application: UIApplication) {
        // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
        // Use this method to pause ongoing tasks, disable timers, and invalidate graphics rendering callbacks. Games should use this method to pause the game.
    }
    
    func applicationDidEnterBackground(_ application: UIApplication) {
        // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
        // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
    }
    
    func applicationWillEnterForeground(_ application: UIApplication) {
        // Called as part of the transition from the background to the active state; here you can undo many of the changes made on entering the background.
    }
    
    
    func applicationWillTerminate(_ application: UIApplication) {
        // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
        // Saves changes in the application's managed object context before the application terminates.
        print(application.debugDescription)
        self.saveContext()
        
        NSSetUncaughtExceptionHandler { exception in
            print(exception.callStackSymbols)
            print(exception.reason!)
            
        }
    }
    
    // MARK: - Core Data stack
    
    lazy var persistentContainer: NSPersistentContainer = {
        /*
         The persistent container for the application. This implementation
         creates and returns a container, having loaded the store for the
         application to it. This property is optional since there are legitimate
         error conditions that could cause the creation of the store to fail.
         */
        let container = NSPersistentContainer(name: "GoGrocery")
        container.loadPersistentStores(completionHandler: { (storeDescription, error) in
            if let error = error as NSError? {
                // Replace this implementation with code to handle the error appropriately.
                // fatalError() causes the application to generate a crash log and terminate. You should not use this function in a shipping application, although it may be useful during development.
                
                /*
                 Typical reasons for an error here include:
                 * The parent directory does not exist, cannot be created, or disallows writing.
                 * The persistent store is not accessible, due to permissions or data protection when the device is locked.
                 * The device is out of space.
                 * The store could not be migrated to the current model version.
                 Check the error message to determine what the actual problem was.
                 */
                fatalError("Unresolved error \(error), \(error.userInfo)")
            }
        })
        return container
    }()
    
    // MARK: - Core Data Saving support
    
    func saveContext () {
        let context = persistentContainer.viewContext
        if context.hasChanges {
            do {
                try context.save()
            } catch {
                // Replace this implementation with code to handle the error appropriately.
                // fatalError() causes the application to generate a crash log and terminate. You should not use this function in a shipping application, although it may be useful during development.
                let nserror = error as NSError
                fatalError("Unresolved error \(nserror), \(nserror.userInfo)")
            }
        }
    }
    
    func checkLocation() {
        if  UserDefaults.standard.value(forKey: "location_check") != nil {
            let mainStoryboardIpad : UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
            let initialViewControlleripad = mainStoryboardIpad.instantiateViewController(withIdentifier: "MarkLocationViewController") as! MarkLocationViewController
            initialViewControlleripad.withinApp = true
            let navigationController = UINavigationController(rootViewController: initialViewControlleripad)
            self.window = UIWindow(frame: UIScreen.main.bounds)
            self.window?.makeKeyAndVisible()
            self.window?.rootViewController = navigationController
        }
        else {
            let mainStoryboardIpad : UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
            let initialViewControlleripad = mainStoryboardIpad.instantiateViewController(withIdentifier: "ViewController") as! ViewController
            let navigationController = UINavigationController(rootViewController: initialViewControlleripad)
            self.window = UIWindow(frame: UIScreen.main.bounds)
            self.window?.makeKeyAndVisible()
            self.window?.rootViewController = navigationController
            
        }
    }
    
}


extension AppDelegate : MessagingDelegate {
    func messaging(_ messaging: Messaging, didReceiveRegistrationToken fcmToken: String)
    {
        print("Firebase registration token: \(fcmToken)")
        print(fcmToken)
        
        let data1 = "\(fcmToken)"
        UserDefaults.standard.setValue(data1, forKey: "fcm_token")
        // UserDefaults.standard.set(data1, forKey: "fcm_token")
        UserDefaults.standard.synchronize()
    }
}
@available(iOS 10, *)
extension AppDelegate : UNUserNotificationCenterDelegate {
    
    // Receive displayed notifications for iOS 10 devices.
    func userNotificationCenter(_ center: UNUserNotificationCenter,
                                willPresent notification: UNNotification,
                                withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void) {
        let userInfo = JSON(notification.request.content.userInfo)
        print(userInfo)
        //        let orderId = userInfo["order_id"].string ?? " "
        //        let mainStoryboardIpad : UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        //         let initialViewControlleripad = mainStoryboardIpad.instantiateViewController(withIdentifier: "OrderDetailsViewController") as! OrderDetailsViewController
        //        initialViewControlleripad.orderId = orderId
        //        initialViewControlleripad.isFromPush = "Push"
        UIApplication.shared.applicationIconBadgeNumber = 0
        //        let navigationController = UINavigationController(rootViewController: initialViewControlleripad)
        //        self.window = UIWindow(frame: UIScreen.main.bounds)
        //          self.window?.makeKeyAndVisible()
        //        self.window?.rootViewController = navigationController
        completionHandler([.alert,.sound,.badge])
    }
    
    func userNotificationCenter(_ center: UNUserNotificationCenter, didReceive response: UNNotificationResponse, withCompletionHandler completionHandler: @escaping () -> Void) {
        let userInfo =  JSON(response.notification.request.content.userInfo)
        print(userInfo)
        let orderId = userInfo["order_id"].intValue
        let noti_type = userInfo["noti_type"].string ?? " "
        if noti_type == "Place Order" {
            if UserDefaults.standard.value(forKey: "is-login") != nil {
                if UserDefaults.standard.value(forKey: "is-login") as! Bool {
                    let mainStoryboardIpad : UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                    let initialViewControlleripad = mainStoryboardIpad.instantiateViewController(withIdentifier: "OrderDetailsViewController") as! OrderDetailsViewController
                    initialViewControlleripad.orderId = "\(orderId)"
                    initialViewControlleripad.isFromPush = "Push"
                    UIApplication.shared.applicationIconBadgeNumber = 0
                    let navigationController = UINavigationController(rootViewController: initialViewControlleripad)
                    self.window = UIWindow(frame: UIScreen.main.bounds)
                    self.window?.makeKeyAndVisible()
                    self.window?.rootViewController = navigationController
                }
                else {
                    let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
                    let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
                    let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                    navigationController.pushViewController(viewController, animated: true)
                }
            }
        }
        if noti_type == "Order Substitute" {
            if UserDefaults.standard.value(forKey: "is-login") != nil {
                if UserDefaults.standard.value(forKey: "is-login") as! Bool {
                    let mainStoryboardIpad : UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                    let initialViewControlleripad = mainStoryboardIpad.instantiateViewController(withIdentifier: "SubstituteViewController") as! SubstituteViewController
                    initialViewControlleripad.orderId = orderId
                    // initialViewControlleripad.isFromPush = "Push"
                    UIApplication.shared.applicationIconBadgeNumber = 0
                    let navigationController = UINavigationController(rootViewController: initialViewControlleripad)
                    self.window = UIWindow(frame: UIScreen.main.bounds)
                    self.window?.makeKeyAndVisible()
                    self.window?.rootViewController = navigationController
                }
                else {
                    let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
                    let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
                    let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                    navigationController.pushViewController(viewController, animated: true)
                }
            }
            
        }
        if noti_type == "Order Picked" {
            if UserDefaults.standard.value(forKey: "is-login") != nil {
                if UserDefaults.standard.value(forKey: "is-login") as! Bool {
                    let mainStoryboardIpad : UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                    let initialViewControlleripad = mainStoryboardIpad.instantiateViewController(withIdentifier: "OrderDetailsViewController") as! OrderDetailsViewController
                    initialViewControlleripad.orderId = "\(orderId)"
                    initialViewControlleripad.isFromPush = "Push"
                    UIApplication.shared.applicationIconBadgeNumber = 0
                    let navigationController = UINavigationController(rootViewController: initialViewControlleripad)
                    self.window = UIWindow(frame: UIScreen.main.bounds)
                    self.window?.makeKeyAndVisible()
                    self.window?.rootViewController = navigationController
                }
                else {
                    let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
                    let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
                    let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                    navigationController.pushViewController(viewController, animated: true)
                }
            }
        }
        //        if noti_type == "Place Order" {
        //                  let mainStoryboardIpad : UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        //                   let initialViewControlleripad = mainStoryboardIpad.instantiateViewController(withIdentifier: "OrderDetailsViewController") as! OrderDetailsViewController
        //                  initialViewControlleripad.orderId = orderId
        //                  initialViewControlleripad.isFromPush = "Push"
        //                  UIApplication.shared.applicationIconBadgeNumber = 0
        //                  let navigationController = UINavigationController(rootViewController: initialViewControlleripad)
        //                  self.window = UIWindow(frame: UIScreen.main.bounds)
        //                    self.window?.makeKeyAndVisible()
        //                  self.window?.rootViewController = navigationController
        //              }
        //        if noti_type == "Place Order" {
        //                  let mainStoryboardIpad : UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        //                   let initialViewControlleripad = mainStoryboardIpad.instantiateViewController(withIdentifier: "OrderDetailsViewController") as! OrderDetailsViewController
        //                  initialViewControlleripad.orderId = orderId
        //                  initialViewControlleripad.isFromPush = "Push"
        //                  UIApplication.shared.applicationIconBadgeNumber = 0
        //                  let navigationController = UINavigationController(rootViewController: initialViewControlleripad)
        //                  self.window = UIWindow(frame: UIScreen.main.bounds)
        //                    self.window?.makeKeyAndVisible()
        //                  self.window?.rootViewController = navigationController
        //              }
        
    }
    func application(_ application: UIApplication, didReceiveRemoteNotification userInfo: [AnyHashable : Any], fetchCompletionHandler completionHandler: @escaping (UIBackgroundFetchResult) -> Void) {
        let userInfo = JSON(userInfo)
        print(userInfo)
        let orderId = userInfo["order_id"].intValue
        let noti_type = userInfo["noti_type"].string ?? " "
        if noti_type == "Place Order" {
            if UserDefaults.standard.value(forKey: "is-login") != nil {
                if UserDefaults.standard.value(forKey: "is-login") as! Bool {
                    let mainStoryboardIpad : UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                    let initialViewControlleripad = mainStoryboardIpad.instantiateViewController(withIdentifier: "OrderDetailsViewController") as! OrderDetailsViewController
                    initialViewControlleripad.orderId = "\(orderId)"
                    initialViewControlleripad.isFromPush = "Push"
                    UIApplication.shared.applicationIconBadgeNumber = 0
                    let navigationController = UINavigationController(rootViewController: initialViewControlleripad)
                    self.window = UIWindow(frame: UIScreen.main.bounds)
                    self.window?.makeKeyAndVisible()
                    self.window?.rootViewController = navigationController
                }
                else {
                    let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
                    let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
                    let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                    navigationController.pushViewController(viewController, animated: true)
                }
            }
        }
        if noti_type == "Order Substitute" {
            if UserDefaults.standard.value(forKey: "is-login") != nil {
                if UserDefaults.standard.value(forKey: "is-login") as! Bool {
                    let mainStoryboardIpad : UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                    let initialViewControlleripad = mainStoryboardIpad.instantiateViewController(withIdentifier: "SubstituteViewController") as! SubstituteViewController
                    initialViewControlleripad.orderId = orderId
                    // initialViewControlleripad.isFromPush = "Push"
                    UIApplication.shared.applicationIconBadgeNumber = 0
                    let navigationController = UINavigationController(rootViewController: initialViewControlleripad)
                    self.window = UIWindow(frame: UIScreen.main.bounds)
                    self.window?.makeKeyAndVisible()
                    self.window?.rootViewController = navigationController
                }
                else {
                    let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
                    let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
                    viewController.orderIdForSubstitute = orderId
                    viewController.isForSubstitute = true
                    let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                    navigationController.pushViewController(viewController, animated: true)
                }
            }
            
        }
        if noti_type == "Order Picked" {
            if UserDefaults.standard.value(forKey: "is-login") != nil {
                if UserDefaults.standard.value(forKey: "is-login") as! Bool {
                    let mainStoryboardIpad : UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
                    let initialViewControlleripad = mainStoryboardIpad.instantiateViewController(withIdentifier: "OrderDetailsViewController") as! OrderDetailsViewController
                    initialViewControlleripad.orderId = "\(orderId)"
                    initialViewControlleripad.isFromPush = "Push"
                    UIApplication.shared.applicationIconBadgeNumber = 0
                    let navigationController = UINavigationController(rootViewController: initialViewControlleripad)
                    self.window = UIWindow(frame: UIScreen.main.bounds)
                    self.window?.makeKeyAndVisible()
                    self.window?.rootViewController = navigationController
                }
                else {
                    let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
                    let viewController = storyboard.instantiateViewController(withIdentifier: "LoginViewController" ) as! LoginViewController
                    let navigationController = UIApplication.shared.keyWindow?.rootViewController as! UINavigationController
                    navigationController.pushViewController(viewController, animated: true)
                }
            }
        }
        //        if noti_type == "Place Order" {
        //                  let mainStoryboardIpad : UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        //                   let initialViewControlleripad = mainStoryboardIpad.instantiateViewController(withIdentifier: "OrderDetailsViewController") as! OrderDetailsViewController
        //                  initialViewControlleripad.orderId = orderId
        //                  initialViewControlleripad.isFromPush = "Push"
        //                  UIApplication.shared.applicationIconBadgeNumber = 0
        //                  let navigationController = UINavigationController(rootViewController: initialViewControlleripad)
        //                  self.window = UIWindow(frame: UIScreen.main.bounds)
        //                    self.window?.makeKeyAndVisible()
        //                  self.window?.rootViewController = navigationController
        //              }
        //        if noti_type == "Place Order" {
        //                  let mainStoryboardIpad : UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        //                   let initialViewControlleripad = mainStoryboardIpad.instantiateViewController(withIdentifier: "OrderDetailsViewController") as! OrderDetailsViewController
        //                  initialViewControlleripad.orderId = orderId
        //                  initialViewControlleripad.isFromPush = "Push"
        //                  UIApplication.shared.applicationIconBadgeNumber = 0
        //                  let navigationController = UINavigationController(rootViewController: initialViewControlleripad)
        //                  self.window = UIWindow(frame: UIScreen.main.bounds)
        //                    self.window?.makeKeyAndVisible()
        //                  self.window?.rootViewController = navigationController
        //              }
    }
}

