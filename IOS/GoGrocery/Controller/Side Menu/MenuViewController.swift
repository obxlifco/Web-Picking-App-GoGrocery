//
//  MenuViewController.swift
//  SlideInTransition
//
//  Created by jay's on 17/12/19
//  Copyright © 2019 jay's. All rights reserved.
//

import UIKit
import AVKit
import SwiftyJSON

//enum MenuType: Int {
//    case shanu
//    case step2
//    case step3
//    case step4
//    case step5
//    case step6
//    case step7
//    case step8
//    case step9
//    case step10
//    case step11
//    case step12
//    case step13
//    case step14
//    case step15
//    case step16
//    case step17
//    case step18
//}


class MenuViewController: UITableViewController {
    var mainMenuNameArray = NSMutableArray()
    var mainMenuArray = NSArray()
    var cmsMenuArray = NSArray()
    var subMenuArray = NSArray()
  //  var didTapMenuType: ((MenuType) -> Void)?
    override func viewDidLoad() {
        super.viewDidLoad()
        ApiCallToGetMenuList()
        // Do any additional setup after loading the view.
    }
    
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.mainMenuArray.count
    }
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "MainMenuTableViewCell", for: indexPath) as! MainMenuTableViewCell
        let MainMenuDict = mainMenuArray[indexPath.row] as! NSDictionary
        print(MainMenuDict)
        cell.lblMainMenuName.text = MainMenuDict["name"]  as? String
        return cell
    }
    override func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        
        let MainMenuDict = mainMenuArray[indexPath.row] as! NSDictionary
        print(MainMenuDict)
        self.subMenuArray = MainMenuDict["child"] as! NSArray
        
//        guard let menuType = MenuType(rawValue: indexPath.row) else { return }
//        dismiss(animated: true) { [weak self] in
//            print("Dismissing: \(menuType)")
//            self?.didTapMenuType?(menuType)
//        }
    }
    
    func ApiCallToGetMenuList() {
        let para : [String : Any] = ["warehouse_id": 4,"lang_code": "en","website_id": 1]
        requestWith(endUrl: "menu_bar/", imageData: nil, parameters: para, onCompletion: { (response) in
            print(response!)
            if (response!["status"] as! NSNumber) == 1 {
                self.mainMenuArray = (response!["menu_bar"] as! NSArray)
                self.cmsMenuArray = (response!["cms_menu"] as! NSArray)
                
                for index in 0..<self.mainMenuArray.count {
                    let dict = self.mainMenuArray[index] as! NSDictionary
                    self.mainMenuNameArray.add(dict["name"] as! String)
                }
                print(self.mainMenuNameArray)
                self.tableView.delegate = self
                self.tableView.dataSource = self
                self.tableView.reloadData()
            }
            else {
                createalert(title: "Alert", message: "Unable to fetch data", vc: self)
            }
        }) { (error) in
//            print(error?.localizedDescription!)
        }
}
}

//extension  UIViewController {
//    
//    func transitionToNew(_ menuType: MenuType) {
//        print(menuType)
//        print(menuType.rawValue)
//        
//
//        let numberofsubcell = [["title":"jay 1","numberofsubcell":["A1","A2"]],["title":"jay 2","numberofsubcell":["B1","B2"]],["title":"jay 2","numberofsubcell":["C1","C2"]]]
//        switch menuType {
//        case .step1:
//              let vc = UIStoryboard(name: "Home", bundle: nil).instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
//            //  vc.submenulist = numberofsubcell[0]
//              self.navigationController?.pushViewController(vc, animated: true)
//        case .step2:
//            let vc = UIStoryboard(name: "Home", bundle: nil).instantiateViewController(withIdentifier: "subMenuViewController") as! subMenuViewController
//             vc.submenulist = numberofsubcell[1]
//            self.navigationController?.pushViewController(vc, animated: true)
//        case .step3:
//            let vc = UIStoryboard(name: "Home", bundle: nil).instantiateViewController(withIdentifier: "subMenuViewController") as! subMenuViewController
//             vc.submenulist = numberofsubcell[2]
//            self.navigationController?.pushViewController(vc, animated: true)
//            case .step4:
//                let vc = UIStoryboard(name: "Home", bundle: nil).instantiateViewController(withIdentifier: "subMenuViewController") as! subMenuViewController
//                 vc.submenulist = numberofsubcell[2]
//                self.navigationController?.pushViewController(vc, animated: true)
//            case .step5:
//                let vc = UIStoryboard(name: "Home", bundle: nil).instantiateViewController(withIdentifier: "subMenuViewController") as! subMenuViewController
//                 vc.submenulist = numberofsubcell[2]
//                self.navigationController?.pushViewController(vc, animated: true)
//            case .step6:
//                let vc = UIStoryboard(name: "Home", bundle: nil).instantiateViewController(withIdentifier: "subMenuViewController") as! subMenuViewController
//                 vc.submenulist = numberofsubcell[2]
//                self.navigationController?.pushViewController(vc, animated: true)
//            case .step7:
//                let vc = UIStoryboard(name: "Home", bundle: nil).instantiateViewController(withIdentifier: "subMenuViewController") as! subMenuViewController
//                 vc.submenulist = numberofsubcell[2]
//                self.navigationController?.pushViewController(vc, animated: true)
//            case .step8:
//                let vc = UIStoryboard(name: "Home", bundle: nil).instantiateViewController(withIdentifier: "subMenuViewController") as! subMenuViewController
//                 vc.submenulist = numberofsubcell[2]
//                self.navigationController?.pushViewController(vc, animated: true)
//            case .step9:
//                let vc = UIStoryboard(name: "Home", bundle: nil).instantiateViewController(withIdentifier: "subMenuViewController") as! subMenuViewController
//                 vc.submenulist = numberofsubcell[2]
//                self.navigationController?.pushViewController(vc, animated: true)
//            case .step10:
//                let vc = UIStoryboard(name: "Home", bundle: nil).instantiateViewController(withIdentifier: "subMenuViewController") as! subMenuViewController
//                 vc.submenulist = numberofsubcell[2]
//                self.navigationController?.pushViewController(vc, animated: true)
//            case .step11:
//                let vc = UIStoryboard(name: "Home", bundle: nil).instantiateViewController(withIdentifier: "subMenuViewController") as! subMenuViewController
//                 vc.submenulist = numberofsubcell[2]
//                self.navigationController?.pushViewController(vc, animated: true)
//            case .step12:
//                let vc = UIStoryboard(name: "Home", bundle: nil).instantiateViewController(withIdentifier: "subMenuViewController") as! subMenuViewController
//                 vc.submenulist = numberofsubcell[2]
//                self.navigationController?.pushViewController(vc, animated: true)
//            case .step13:
//                let vc = UIStoryboard(name: "Home", bundle: nil).instantiateViewController(withIdentifier: "subMenuViewController") as! subMenuViewController
//                 vc.submenulist = numberofsubcell[2]
//                self.navigationController?.pushViewController(vc, animated: true)
//            case .step14:
//                let vc = UIStoryboard(name: "Home", bundle: nil).instantiateViewController(withIdentifier: "subMenuViewController") as! subMenuViewController
//                 vc.submenulist = numberofsubcell[2]
//                self.navigationController?.pushViewController(vc, animated: true)
//            case .step15:
//                let vc = UIStoryboard(name: "Home", bundle: nil).instantiateViewController(withIdentifier: "subMenuViewController") as! subMenuViewController
//                 vc.submenulist = numberofsubcell[2]
//                self.navigationController?.pushViewController(vc, animated: true)
//            case .step16:
//                let vc = UIStoryboard(name: "Home", bundle: nil).instantiateViewController(withIdentifier: "subMenuViewController") as! subMenuViewController
//                 vc.submenulist = numberofsubcell[2]
//                self.navigationController?.pushViewController(vc, animated: true)
//            case .step17:
//                let vc = UIStoryboard(name: "Home", bundle: nil).instantiateViewController(withIdentifier: "subMenuViewController") as! subMenuViewController
//                 vc.submenulist = numberofsubcell[2]
//                self.navigationController?.pushViewController(vc, animated: true)
//            case .step18:
//                let vc = UIStoryboard(name: "Home", bundle: nil).instantiateViewController(withIdentifier: "subMenuViewController") as! subMenuViewController
//                 vc.submenulist = numberofsubcell[2]
//                self.navigationController?.pushViewController(vc, animated: true)
//        default:
//            break
//        }
//    }
//}


