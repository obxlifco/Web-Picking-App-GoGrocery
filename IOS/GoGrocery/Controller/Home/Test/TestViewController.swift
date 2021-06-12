//
//  TestViewController.swift
//  GoGrocery
//
//  Created by NAV63 on 25/08/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class TestViewController: UIViewController {

   
    @IBOutlet weak var testTableView: UITableView!
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }
}
extension TestViewController : UITableViewDelegate, UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 10
    }
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
          return 300
      }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "TestTableViewCell", for: indexPath) as! TestTableViewCell
        return cell
    }
    func tableView(_ tableView: UITableView, willDisplay cell: UITableViewCell, forRowAt indexPath: IndexPath) {
       // let cell = tableView.dequeueReusableCell(withIdentifier: "TestTableViewCell") as! TestTableViewCell
        guard let cell = cell as? TestTableViewCell else { return }
        cell.testCollectionView.register(TestCollectionViewCell.self, forCellWithReuseIdentifier: "TestCollectionViewCell")
        cell.testCollectionView.dataSource = self
        cell.testCollectionView.delegate = self
        cell.testCollectionView.reloadData()
    }
}

extension TestViewController : UICollectionViewDelegate, UICollectionViewDataSource {
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return 10
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "TestCollectionViewCell", for: indexPath) as! TestCollectionViewCell
        cell.backgroundColor = .red
        cell.isHidden = false
        cell.alpha = 1
        return cell
    }
    
    
}
extension TestViewController : UICollectionViewDelegateFlowLayout {
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
//        let numberOfItemsPerRow:CGFloat = 2
//        let spacingBetweenCells:CGFloat = 1
//
//        let totalSpacing = (2 * self.spacing) + ((numberOfItemsPerRow - 1) * spacingBetweenCells) //Amount of total spacing in a row
//
//        if let collection = self.repTableView {
//            let width = (collection.bounds.width - totalSpacing)/numberOfItemsPerRow
//            return CGSize(width: width, height: 320)
//        }
//        else{
//            return CGSize(width: 0, height: 0)
//        }
// */
         return CGSize(width: 150, height: 150)
    }
    
}

