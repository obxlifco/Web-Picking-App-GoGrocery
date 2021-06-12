//
//  UICollectionView+Extension.swift
//  GoGrocery
//
//  Created by NAV63 on 25/08/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import Foundation
import UIKit

extension UICollectionView {
    func registerNibForCell<T: UICollectionViewCell>(_ cell: T.Type) {
        let cellNib = UINib(nibName: T.nameOfClass, bundle: nil)
        register(cellNib, forCellWithReuseIdentifier: T.nameOfClass)
    }
    
    func registerNibForSupplementaryView<T: UICollectionReusableView>(_ cell: T.Type, of kind: String) {
        let cellNib = UINib(nibName: T.nameOfClass, bundle: nil)
        register(cellNib, forSupplementaryViewOfKind: kind, withReuseIdentifier: T.nameOfClass)
    }
    
    func dequeueReusableCellForIndexPath<T: UICollectionViewCell>(_ indexPath: IndexPath) -> T {
        return dequeueReusableCell(withReuseIdentifier: T.nameOfClass, for: indexPath) as! T
    }
    func dequeueReusableSupplementaryViewForIndexPath<T: UICollectionReusableView>(_ indexPath: IndexPath, of kind: String) -> T {
        return dequeueReusableSupplementaryView(ofKind: kind, withReuseIdentifier: T.nameOfClass, for: indexPath) as! T
    }
}
extension UIView {
    static var nameOfClass: String {
        return String(describing: self)
    }
    
    var nameOfClass: String {
        return String(describing: type(of: self))
    }
}
