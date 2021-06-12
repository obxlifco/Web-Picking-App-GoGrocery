//
//  NoWarehouse.swift
//  GoGrocery
//
//  Created by NAV63 on 17/03/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class NoWarehouse: UIView {

    @IBOutlet weak var btnChaneLocation: UIButton!
    @IBOutlet weak var viewWareHouse: UIView!
    
}
var NowareHouseXib = NoWarehouse()
func requestNoWareHouseView(vc: UIViewController){
    
    NowareHouseXib.removeFromSuperview() // make it only once
    NowareHouseXib = Bundle.main.loadNibNamed("NoWareHouse", owner: vc, options: nil)?.first as! NoWarehouse
    NowareHouseXib.frame = CGRect(x:0, y: 0, width: UIScreen.main.bounds.size.width, height: UIScreen.main.bounds.size.height)
    NowareHouseXib.alpha = 0
    
    UIView.animate(withDuration: 0.5) {
        NowareHouseXib.alpha = 1
    }
    appdelegate.window?.addSubview(NowareHouseXib)
}
