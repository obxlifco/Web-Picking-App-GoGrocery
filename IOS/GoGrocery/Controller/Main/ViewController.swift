import UIKit
import CoreLocation
import GoogleMaps
import GooglePlaces
class ViewController: UIViewController,CLLocationManagerDelegate {
    //MARK:- Outlet Declaration
    @IBOutlet weak var btnEnableLocation: UIButton!
    //MARK:- Variable Declaration
    var locationManager = CLLocationManager()
    // MARK:- View Lifecycle
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.navigationController?.isNavigationBarHidden = true
        btnEnableLocation.layer.cornerRadius = 5
        btnEnableLocation.layer.borderColor = UIColor.white.cgColor
        btnEnableLocation.layer.borderWidth = 1
        locationManager.delegate = self
        // Do any additional setup after loading the view, typically from a nib.
    }
    override func viewWillAppear(_ animated: Bool) {
        self.navigationController?.isNavigationBarHidden = true
      //  checkForLocationAuthorization()
    }
    
    @IBAction func btnEnableLocationAction(_ sender: Any) {
    
        let locStatus = CLLocationManager.authorizationStatus()
      switch locStatus {
         case .notDetermined:
            locationManager.requestWhenInUseAuthorization()
        return
         case .denied, .restricted:
            let alert = UIAlertController(title: "Location Services are disabled", message: "Please enable Location Services in your Settings", preferredStyle: .alert)
            let okAction = UIAlertAction(title: "OK", style: .default, handler: nil)
            alert.addAction(okAction)
            present(alert, animated: true, completion: nil)
        return
        case .authorizedAlways, .authorizedWhenInUse:
           let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
            let vc = storyboard.instantiateViewController(withIdentifier: "MarkLocationViewController") as! MarkLocationViewController
            self.navigationController?.pushViewController(vc, animated: true)
         break
      }
 
        
   /*       if CLLocationManager.locationServicesEnabled() {
                self.locationManager.requestAlwaysAuthorization()
                // For use in foreground
                self.locationManager.requestWhenInUseAuthorization()
                locationManager.delegate = self
                locationManager.desiredAccuracy = kCLLocationAccuracyNearestTenMeters
                locationManager.startUpdatingLocation()
            }
            else {
                 let alertController = UIAlertController (title: "GoGrocery requires user’s location to see the nearby by store so they can order products from that nearby store", message: "GoGrocery requires user’s location to see the nearby by store so they can order products from that nearby store", preferredStyle: .alert)

                 let settingsAction = UIAlertAction(title: "Settings", style: .default) { (_) -> Void in
                    guard let settingsUrl = URL(string: UIApplication.openSettingsURLString) else {
                         return
                     }
                     if UIApplication.shared.canOpenURL(settingsUrl) {
                         UIApplication.shared.open(settingsUrl, completionHandler: { (success) in
                             print("Settings opened: \(success)") // Prints true
                         })
                     }
                 }
                 alertController.addAction(settingsAction)
                 let cancelAction = UIAlertAction(title: "Cancel", style: .default, handler: nil)
                 alertController.addAction(cancelAction)

                 present(alertController, animated: true, completion: nil)

        }
 */

    }
    
    func locationManager(_ manager: CLLocationManager, didChangeAuthorization status: CLAuthorizationStatus) {
        if status == .authorizedWhenInUse ||  status == .authorizedAlways  {
            if CLLocationManager.isMonitoringAvailable(for: CLBeaconRegion.self) {
                if CLLocationManager.isRangingAvailable() {
                  /*  let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
                    let vc = storyboard.instantiateViewController(withIdentifier: "MarkLocationViewController") as! MarkLocationViewController
                    self.navigationController?.pushViewController(vc, animated: true) */
                    // do stuff
                }
            }
        }
    }
    
    // 2
    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        print(error)
    }
    
//    func checkForLocationAuthorization() {
//        let location_check = UserDefaults.standard.value(forKey: "location_check")
//        if location_check != nil {
//            if "\(location_check!)" == "1" {
//                let storyboard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
//                let vc = storyboard.instantiateViewController(withIdentifier: "MarkLocationViewController") as! MarkLocationViewController
//
//                self.navigationController?.pushViewController(vc, animated: true)
//            }
//        }
//        else {
//        }
//    }
    
}

