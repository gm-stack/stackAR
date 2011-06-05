// Decompiled by Jad v1.5.8g. Copyright 2001 Pavel Kouznetsov.
// Jad home page: http://www.kpdus.com/jad.html
// Decompiler options: packimports(3) braces deadcode 

package net.minecraft.src;

import java.awt.Component;
import java.nio.IntBuffer;
import org.lwjgl.LWJGLException;
import org.lwjgl.input.Cursor;
import org.lwjgl.input.Mouse;

import java.net.*;
import java.io.*;

// Referenced classes of package net.minecraft.src:
//            GLAllocation

public class MouseHelper
{

    public MouseHelper(Component component)
    {
        field_1115_e = 10;
        field_1117_c = component;
        IntBuffer intbuffer = GLAllocation.createDirectIntBuffer(1);
        intbuffer.put(0);
        intbuffer.flip();
        IntBuffer intbuffer1 = GLAllocation.createDirectIntBuffer(1024);
        try
        {
            cursor = new Cursor(32, 32, 16, 16, 1, intbuffer1, intbuffer);
        }
        catch(LWJGLException lwjglexception)
        {
            lwjglexception.printStackTrace();
        }
        
        try {
            Socket sensorSocket = new Socket("127.0.0.1", 49154);
            socketBuffer = new BufferedReader(new InputStreamReader(sensorSocket.getInputStream()));
            System.out.println("Connected successfully");            
        } catch (IOException e) {
            System.out.println("Error connecting to sensor daemon: ");
            System.out.println(e);
        }
        
    }

    public void grabMouseCursor()
    {
        Mouse.setGrabbed(true);
        deltaX = 0;
        deltaY = 0;
    }

    public void ungrabMouseCursor()
    {
        Mouse.setCursorPosition(field_1117_c.getWidth() / 2, field_1117_c.getHeight() / 2);
        Mouse.setGrabbed(false);
    }

    public void mouseXYChange()
    {
        int Xint = 0;
        int Yint = 0;
        
        try {
            while (socketBuffer.ready()) {
                String line = socketBuffer.readLine();
                //System.out.println("Line: " + line);
                
                String[] ssp = line.split(" ");
                
                Xint -= (Integer.parseInt(ssp[8]-1) * 2);
                Yint -= (Integer.parseInt(ssp[6]) * 2);
            }
        } catch (IOException e) {
        }
        
        deltaX = Mouse.getDX() + Xint;
        deltaY = Mouse.getDY() + Yint;
    }

    private Component field_1117_c;
    private Cursor cursor;
    public int deltaX;
    public int deltaY;
    private int field_1115_e;
    Socket sensorSocket;
    BufferedReader socketBuffer;
}
