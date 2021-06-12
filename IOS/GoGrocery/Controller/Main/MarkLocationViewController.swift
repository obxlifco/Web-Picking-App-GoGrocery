
import UIKit
import GoogleMaps
import GooglePlaces
import SwiftyJSON
import FirebaseCrashlytics
import Crashlytics
class MarkLocationViewController: UIViewController, CLLocationManagerDelegate,UITextFieldDelegate {
    //MARK:- Outlet Declaration
    @IBOutlet weak var mapView: GMSMapView!
    @IBOutlet weak var txtLocation: UITextField!
    @IBOutlet weak var btnTxt: UIButton!
    //MARK:- Variable Declaration
    var locationManager = CLLocationManager()
    var SelectLat = String()
    var SelectLong = String()
    var SelectLatDouble = Double()
    var SelectLongDouble = Double()
    var LatDouble = Double()
    var LongDouble = Double()
    var website_id = String()
    var locationChaneBool = false
    var withinApp = Bool()
    @IBOutlet weak var imgImage: UIImageView!
    // var googleAutoBool = false
    //MARK:- View Lifecycle
    override func viewDidLoad() {
        super.viewDidLoad()
        
//        if withinApp == true {
//            imgImage.isHidden = false
//             ApiCallToCheckAppVersion()
//        }
//        else {
//            imgImage.isHidden = true
//        }
       // imgImage.isHidden = true
        txtLocation.layer.cornerRadius = 5
        txtLocation.layer.borderColor = UIColor(named: "buttonColor")?.cgColor
        txtLocation.layer.borderWidth = 0.5
        txtLocation.delegate = self
        txtLocation.setLeftPaddingPoints(10)
        self.navigationController?.navigationBar.tintColor = .black
        self.navigationController?.navigationBar.titleTextAttributes = [NSAttributedString.Key.foregroundColor: UIColor.black]
        let backButton = UIBarButtonItem()
        backButton.title = ""
        navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
        print("In View Did Load----------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        self.mapView.settings.compassButton = true
        mapView.isMyLocationEnabled = true
        self.mapView.settings.myLocationButton = false
        mapView.delegate = self
        self.mapView.padding = UIEdgeInsets(top: 0, left: 0, bottom: 10, right: 0)
        //locationManager.startUpdatingLocation()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        self.navigationController?.isNavigationBarHidden = true
        if locationChaneBool == false {
            if UserDefaults.standard.value(forKey: "SelectLong") != nil {
                let lat = UserDefaults.standard.value(forKey: "SelectLat") as! String
                let long = UserDefaults.standard.value(forKey: "SelectLong") as! String
                let latD = Double(lat)
                let longD = Double(long)
                let camera = GMSCameraPosition.camera(withLatitude: latD!, longitude: longD!, zoom: 15.0)
                self.mapView?.animate(to: camera)
                getAddressFromLatLon(pdblLatitude: lat, withLongitude: long)
            }
            else {
                locationManager.delegate = self
                locationManager.startUpdatingLocation()
            }
        }
        else {
            print("fdfd")
        }
    }
       func ApiCallToCheckAppVersion() {
           let appVersion = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String
           print(appVersion!)
           getMethodReturnWithoutJson(apiName: "get-app-version/") { (response) in
               print(response)
               if response["status"].intValue == 200 {
                   let data = response["data"].dictionaryValue
                   if data["version_i"]?.stringValue == appVersion {
                    self.imgImage.isHidden = true
                   }
                   else {
                       self.setUpUpdateXibFunc()
                   }
               }
           }
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
    
    func showMapTiles() {
        self.mapView.settings.compassButton = true
        mapView.isMyLocationEnabled = true
        self.mapView.settings.myLocationButton = true
        self.mapView.padding = UIEdgeInsets(top: 0, left: 0, bottom: 10, right: 0)
    }
    
    @IBAction func btnCurrentLocation(_ sender: Any) {
        guard let lat = self.mapView.myLocation?.coordinate.latitude,
              let lng = self.mapView.myLocation?.coordinate.longitude else { return }
        self.SelectLat = "\(self.mapView.myLocation!.coordinate.latitude)"
        self.SelectLong = "\(self.mapView.myLocation!.coordinate.longitude)"
        let camera = GMSCameraPosition.camera(withLatitude: lat ,longitude: lng , zoom: 14.0)
        self.mapView.animate(to: camera)
        getAddressFromLatLon(pdblLatitude: self.SelectLat, withLongitude: self.SelectLong)
    }
    
    @IBAction func confirmLocationBtnAction(_ sender: Any) {
        if txtLocation.text?.isEmpty == false {
  /*
          let vc = self.storyboard?.instantiateViewController(withIdentifier: "SelectCityViewController") as! SelectCityViewController
            self.SelectLatDouble = Double(SelectLat ?? "00.00") as! Double
            self.SelectLongDouble = Double(SelectLong ?? "00.00") as! Double
            self.SelectLat = String(format: "%.9f", SelectLatDouble)
            self.SelectLong = String(format: "%.9f", SelectLongDouble)
//            vc.lat = String(format: "%.9f", SelectLatDouble)
//            vc.long = String(format: "%.9f", SelectLongDouble)
            let backButton = UIBarButtonItem()
            backButton.title = ""
            navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
            UserDefaults.standard.setValue("1", forKey: "location_check")
            UserDefaults.standard.setValue(SelectLat, forKey: "SelectLat")
            UserDefaults.standard.setValue(SelectLong, forKey: "SelectLong")
            UserDefaults.standard.synchronize()
            locationManager.stopUpdatingLocation()
           self.navigationController?.pushViewController(vc, animated: true)
 */
    
            let vc = self.storyboard?.instantiateViewController(withIdentifier: "CategoryViewController") as! CategoryViewController
              self.SelectLatDouble = Double(SelectLat ?? "00.00") as! Double
              self.SelectLongDouble = Double(SelectLong ?? "00.00") as! Double
              self.SelectLat = String(format: "%.9f", SelectLatDouble)
              self.SelectLong = String(format: "%.9f", SelectLongDouble)
              vc.catlat = String(format: "%.9f", SelectLatDouble)
              vc.catlong = String(format: "%.9f", SelectLongDouble)
              let backButton = UIBarButtonItem()
              backButton.title = ""
              navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
              UserDefaults.standard.setValue("1", forKey: "location_check")
              UserDefaults.standard.setValue(SelectLat, forKey: "SelectLat")
              UserDefaults.standard.setValue(SelectLong, forKey: "SelectLong")
              UserDefaults.standard.synchronize()
              locationManager.stopUpdatingLocation()
             self.navigationController?.pushViewController(vc, animated: true)
 
            
//             let storyboard:UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
//             let vc = storyboard.instantiateViewController(withIdentifier: "CategoryViewController") as! CategoryViewController
//             self.navigationController?.pushViewController(vc, animated: true)

     /*
      
             let storyboard:UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
            let vc = storyboard.instantiateViewController(withIdentifier: "SubstituteViewController") as! SubstituteViewController
             self.navigationController?.pushViewController(vc, animated: true)
*/
        }
        else {
            createalert(title: "Alert", message: "Please select location", vc: self)
        }
    }
    //MARK:- did Update Locations
    func showMarker(position: CLLocationCoordinate2D){
        let marker = GMSMarker()
        marker.position = position
        marker.title = "Palo Alto"
        marker.snippet = "San Francisco"
        marker.map = mapView
    }
    @IBAction func btnChangeLocation(_ sender: Any) {
        let placePickerController = GMSAutocompleteViewController()
        placePickerController.delegate = self
       // googleAutoBool = true
        present(placePickerController, animated: true, completion: nil)
    }
    //MARK:- did Update Locations
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let locValue: CLLocationCoordinate2D = manager.location?.coordinate else { return }
        print("locations = \(locValue.latitude) \(locValue.longitude)")
        self.SelectLat = "\(locValue.latitude)"
        self.SelectLong = "\(locValue.longitude)"
        self.SelectLatDouble = locValue.latitude
        self.SelectLongDouble = locValue.longitude
        let camera = GMSCameraPosition.camera(withLatitude: locValue.latitude, longitude: locValue.longitude, zoom: 15.0)
        self.mapView?.animate(to: camera)
        getAddressFromLatLon(pdblLatitude: self.SelectLat, withLongitude: self.SelectLong)
       // locationManager.stopUpdatingLocation()
    }
    // MARK:- Address convert
    func getAddressFromLatLon(pdblLatitude: String, withLongitude pdblLongitude: String) {
        var center : CLLocationCoordinate2D = CLLocationCoordinate2D()
        let lat: Double = Double("\(pdblLatitude)")!
        let lon: Double = Double("\(pdblLongitude)")!
        let ceo: CLGeocoder = CLGeocoder()
        center.latitude = lat
        center.longitude = lon
        let loc: CLLocation = CLLocation(latitude:center.latitude, longitude: center.longitude)
        ceo.reverseGeocodeLocation(loc, completionHandler:
            {(placemarks, error) in
                if (error != nil) {
                    print("reverse geodcode fail: \(error!.localizedDescription)")
                }
                if let pm = placemarks {
                    if pm.count > 0 {
                        let pm = placemarks![0]
                        print(pm)
                        var addressString : String = ""
                        if pm.locality != nil {
                            addressString = addressString + pm.locality! + ", "
                        }
                        if pm.subLocality != nil {
                            addressString = addressString + pm.subLocality! + ", "
                        }
                        if pm.country != nil {
                            addressString = addressString + pm.country! + ", "
                        }
                        if pm.postalCode != nil {
                            addressString = addressString + pm.postalCode! + " "
                        }
                        self.txtLocation.text = addressString
                    }
                }
        })
    }
    
}
extension MarkLocationViewController: GMSAutocompleteViewControllerDelegate {
    // Handle the user's selection.
    func viewController(_ viewController: GMSAutocompleteViewController, didAutocompleteWith place: GMSPlace) {
        self.SelectLat = "\(place.coordinate.latitude)"
        self.SelectLong = "\(place.coordinate.longitude)"
        self.txtLocation.text = "\(place.formattedAddress!)"
        let camera = GMSCameraPosition.camera(withLatitude: place.coordinate.latitude, longitude: place.coordinate.longitude, zoom: 15.0)
        self.mapView?.animate(to: camera)
        print(self.SelectLat )
        print(self.SelectLong)
        UserDefaults.standard.setValue(SelectLat, forKey: "SelectLat")
        UserDefaults.standard.setValue(SelectLong, forKey: "SelectLong")
        UserDefaults.standard.synchronize()
        self.locationChaneBool = true
        locationManager.stopUpdatingLocation()
        dismiss(animated: true, completion: nil)

    }
    func viewController(_ viewController: GMSAutocompleteViewController, didFailAutocompleteWithError error: Error) {
        print("Error: ", error.localizedDescription)
    }
    // User canceled the operation.
    func wasCancelled(_ viewController: GMSAutocompleteViewController) {
        dismiss(animated: true, completion: nil)
    }
    // Turn the network activity indicator on and off again.
    func didRequestAutocompletePredictions(_ viewController: GMSAutocompleteViewController) {
        UIApplication.shared.isNetworkActivityIndicatorVisible = true
    }
    func didUpdateAutocompletePredictions(_ viewController: GMSAutocompleteViewController) {
        UIApplication.shared.isNetworkActivityIndicatorVisible = false
    }
    
}
extension MarkLocationViewController: GMSMapViewDelegate{
    //MARK - GMSMarker Dragging
    func mapView(_ mapView: GMSMapView, idleAt cameraPosition: GMSCameraPosition) {
        print("cameraPosition =====> \(cameraPosition)")
        self.SelectLat = "\(mapView.camera.target.latitude)"
        self.SelectLong = "\(mapView.camera.target.longitude)"
        getAddressFromLatLon(pdblLatitude: self.SelectLat, withLongitude: self.SelectLong)
    }
}
