//
//  SusbtituteViewController.swift
//  GoGrocery
//
//  Created by NAV63 on 28/08/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
class SusbtituteSucccessViewController: UIViewController {

       @IBOutlet weak var btnContinueShopping: UIButton!
    override func viewDidLoad() {
        super.viewDidLoad()

        self.btnContinueShopping.layer.cornerRadius = 5
         self.btnContinueShopping.layer.borderColor = UIColor(named: "buttonBackgroundColor")?.cgColor
         self.btnContinueShopping.layer.borderWidth = 1
         self.btnContinueShopping.setTitle("CONTINUE SHOPPING", for: .normal)
         self.btnContinueShopping.setTitleColor(UIColor(named: "buttonBackgroundColor"), for: .normal)
        // PurchaseEvent(order_id : "\(orderId)")
        // Do any additional setup after loading the view.
    }
    
    @IBAction func btnContinueShoppingAction(_ sender: Any) {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
        self.navigationController?.pushViewController(vc, animated: true)
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
