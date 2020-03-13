package com.example.image;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;

import android.provider.MediaStore;
import android.util.Log;
import android.view.View;


import android.widget.Toast;
import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.LoaderCallbackInterface;
import org.opencv.android.OpenCVLoader;
import org.opencv.android.Utils;
import org.opencv.core.CvType;
import org.opencv.core.Mat;

import java.io.ByteArrayOutputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;


public class MainActivity extends AppCompatActivity {

    public static Bitmap IMGbitmap,IMGbitmapOG;
    public static Mat IMGmat;


    private BaseLoaderCallback mLoaderCallback = new BaseLoaderCallback(this) {
        @Override
        public void onManagerConnected(int status) {
            switch (status) {
                case LoaderCallbackInterface.SUCCESS:
                {Toast.makeText(getApplicationContext(),"Yes",Toast.LENGTH_SHORT).show();
                    Log.i("OpenCV", "OpenCV loaded successfully");

                } break;
                default:
                {Toast.makeText(getApplicationContext(),"NO",Toast.LENGTH_SHORT).show();
                    super.onManagerConnected(status);

                } break;
            }
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void importIMG(View view) {
        Intent PhotoPick = new Intent(Intent.ACTION_PICK);
        PhotoPick.setType("image/*");
        startActivityForResult(PhotoPick,1);
    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data)
    {
        super.onActivityResult(requestCode,resultCode,data);
        if(resultCode==RESULT_OK){
            if(requestCode==1){
                try{
                    Uri imguri = data.getData();

                    InputStream imgstrm = getContentResolver().openInputStream(imguri);
                    IMGbitmap = BitmapFactory.decodeStream(imgstrm);
                    IMGbitmapOG = Bitmap.createBitmap(IMGbitmap);
                    Bitmap2Mat();
                    Intent i1 = new Intent(this,ImageViewArea.class);
                    startActivity(i1);
                }
                catch (FileNotFoundException e) {
                    e.printStackTrace();
                    Toast.makeText(getApplicationContext(),"Oops,Something went Wrong!!",Toast.LENGTH_SHORT).show();
                }
            }
            else if(requestCode ==2){
                Bundle extras = data.getExtras();
                IMGbitmap = (Bitmap)extras.get("data");
                Bitmap2Mat();
                IMGbitmapOG = Bitmap.createBitmap(IMGbitmap);
                Intent i1 = new Intent(this,ImageViewArea.class);
                startActivity(i1);
            }
        }
        else
        {
            Toast.makeText(getApplicationContext(),"Pick any Image",Toast.LENGTH_SHORT).show();
        }
    }

    public void takePhoto(View view) {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if(takePictureIntent.resolveActivity(getPackageManager())!= null){
            startActivityForResult(takePictureIntent,2);
        }
    }





    public void Bitmap2Mat() {
        IMGbitmap = IMGbitmap.copy(Bitmap.Config.ARGB_8888, true);
        Mat IMGmatCpy = new Mat(IMGbitmap.getHeight(), IMGbitmap.getWidth(), CvType.CV_8UC4);
        Utils.bitmapToMat(IMGbitmap, IMGmatCpy);
        IMGmat = IMGmatCpy.clone();
        System.out.println("******************************************************************************"+IMGmat.cols() + "x" + IMGmat.rows());
    }

    public void onResume()
    {
        super.onResume();
        if (!OpenCVLoader.initDebug()) {
            Log.d("OpenCV", "Internal OpenCV library not found. Using OpenCV Manager for initialization");
            OpenCVLoader.initAsync(OpenCVLoader.OPENCV_VERSION_3_0_0, this, mLoaderCallback);
        } else {
            Log.d("OpenCV", "OpenCV library found inside package. Using it!");
            mLoaderCallback.onManagerConnected(LoaderCallbackInterface.SUCCESS);
        }
    }


}


