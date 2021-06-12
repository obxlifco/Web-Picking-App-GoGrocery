//
//  MainCollectionViewCell.swift
//  GoGrocery
//
//  Created by NAV63 on 26/08/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class MainCollectionViewCell: UICollectionViewCell {
      @IBOutlet weak var subsCollectionView: UICollectionView!
    
    @IBOutlet weak var imgMain: UIImageView!
    @IBOutlet weak var lblOutOfStock: UILabel!
    @IBOutlet weak var lblProductName: UILabel!
    @IBOutlet weak var lblProductPrice: UILabel!
    @IBOutlet weak var lblProductWeight: UILabel!
    @IBOutlet weak var lblProductMaxQuantity: UILabel!
     @IBOutlet weak var lblChooseAReplacement: UILabel!
    
    @IBOutlet weak var submittedView: UIView!
    
    
}
