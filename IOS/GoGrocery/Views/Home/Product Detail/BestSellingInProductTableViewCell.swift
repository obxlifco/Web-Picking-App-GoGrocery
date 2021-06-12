//
//  BestSellingInProductTableViewCell.swift
//  GoGrocery
//
//  Created by NAV63 on 09/04/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class BestSellingInProductTableViewCell: UITableViewCell {
    
    @IBOutlet weak var bestCollectionView: UICollectionView!
    var screenSize: CGRect!
    var screenWidth: CGFloat!
    var screenHeight: CGFloat!
       private let spacing:CGFloat = 16
    
    override func awakeFromNib() {
        super.awakeFromNib()


    }
    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
