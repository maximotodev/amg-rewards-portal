import { Component } from '@angular/core';
import { ReceiptFormComponent } from './components/receipt-form/receipt-form';
import { ReceiptListComponent } from './components/receipt-list/receipt-list';

@Component({
  selector: 'amg-root',
  standalone: true,
  // We add our components to the imports array here
  imports: [ReceiptFormComponent, ReceiptListComponent],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  // We can keep this clean for the demo
  title = 'AMG Rewards Portal';
}
