const std = @import("std");

const converter = @import("converter");

const zglfw = @import("zglfw");
const zgpu = @import("zgpu");
const wgpu = zgpu.wgpu;
const zgui = @import("zgui");

const Settings = struct {
    input_folder_path: []const u8 = "",
    output_folder_path: []const u8 = "",
    game_executable_path: []const u8 = "",
    beautify_lua: bool = true,
};

pub fn main() !void {
    zglfw.init() catch {
        std.log.err("Failed to initialize GLFW library.", .{});
        return;
    };
    defer zglfw.terminate();

    const window = zglfw.Window.create(1600, 300, "Legacy Mod Converter v1.2 for CCCP release 6", null) catch {
        std.log.err("Failed to create window.", .{});
        return;
    };
    defer window.destroy();
    // window.setSizeLimits(600, 400, -1, -1);

    var gpa_state = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa_state.deinit();
    const gpa = gpa_state.allocator();

    const gctx = try zgpu.GraphicsContext.create(gpa, .{
        .window = window,
        .fn_getTime = @ptrCast(&zglfw.getTime),
        .fn_getFramebufferSize = @ptrCast(&zglfw.Window.getFramebufferSize),
        .fn_getWin32Window = @ptrCast(&zglfw.getWin32Window),
        .fn_getX11Display = @ptrCast(&zglfw.getX11Display),
        .fn_getX11Window = @ptrCast(&zglfw.getX11Window),
        .fn_getWaylandDisplay = @ptrCast(&zglfw.getWaylandDisplay),
        .fn_getWaylandSurface = @ptrCast(&zglfw.getWaylandWindow),
        .fn_getCocoaWindow = @ptrCast(&zglfw.getCocoaWindow),
    }, .{});
    defer gctx.destroy(gpa);

    zgui.init(gpa);
    defer zgui.deinit();

    _ = zgui.io.addFontFromFile("fonts/ProggyClean.ttf", 26.0);

    zgui.backend.init(
        window,
        gctx.device,
        @intFromEnum(zgpu.GraphicsContext.swapchain_format),
        @intFromEnum(wgpu.TextureFormat.undef),
    );
    defer zgui.backend.deinit();

    const settings_text = std.fs.cwd().readFileAlloc(gpa, "settings.json", 1337) catch |err| switch (err) {
        error.FileNotFound => try gpa.dupe(u8, "{}"),
        else => return err,
    };
    defer gpa.free(settings_text);

    const settings_parsed = try std.json.parseFromSlice(Settings, gpa, settings_text, .{});
    defer settings_parsed.deinit();
    var settings = settings_parsed.value;

    var input_folder_path_mut: [std.fs.MAX_PATH_BYTES + 1:0]u8 = undefined;
    @memcpy(input_folder_path_mut[0..settings.input_folder_path.len], settings.input_folder_path);
    input_folder_path_mut[settings.input_folder_path.len] = 0;

    var output_folder_path_mut: [std.fs.MAX_PATH_BYTES + 1:0]u8 = undefined;
    @memcpy(output_folder_path_mut[0..settings.output_folder_path.len], settings.output_folder_path);
    output_folder_path_mut[settings.output_folder_path.len] = 0;

    var game_executable_path_mut: [std.fs.MAX_PATH_BYTES + 1:0]u8 = undefined;
    @memcpy(game_executable_path_mut[0..settings.game_executable_path.len], settings.game_executable_path);
    game_executable_path_mut[settings.game_executable_path.len] = 0;

    var popup_buf: [420420]u8 = undefined;
    var popup_slice: []u8 = undefined;

    while (!window.shouldClose()) {
        zglfw.pollEvents();

        zgui.backend.newFrame(
            gctx.swapchain_descriptor.width,
            gctx.swapchain_descriptor.height,
        );

        // Set the starting window position and size to custom values
        zgui.setNextWindowPos(.{ .x = 0.0, .y = 0.0, .cond = .always });
        zgui.setNextWindowSize(.{ .w = -1.0, .h = -1.0, .cond = .always });
        // zgui.setNextWindowSize(.{ .w = 420, .h = 300, .cond = .always });

        if (zgui.begin("invisible_title", .{ .flags = .{ .no_title_bar = true, .no_resize = true, .no_background = true } })) {
            const padding = 15;
            const min_width = 855;

            zgui.setNextItemWidth(@max(zgui.calcTextSize(settings.input_folder_path, .{})[0] + padding, min_width));
            if (zgui.inputTextWithHint("Input/ folder path", .{ .hint = "Copy-paste a path from File Explorer here", .buf = &input_folder_path_mut })) {
                settings.input_folder_path = std.mem.span(@as([*:0]u8, &input_folder_path_mut));
                try writeSettings(settings);
            }

            zgui.setNextItemWidth(@max(zgui.calcTextSize(settings.output_folder_path, .{})[0] + padding, min_width));
            if (zgui.inputTextWithHint("Mods/ folder path", .{ .hint = "Copy-paste a path from File Explorer here", .buf = &output_folder_path_mut })) {
                settings.output_folder_path = std.mem.span(@as([*:0]u8, &output_folder_path_mut));
                try writeSettings(settings);
            }

            if (zgui.checkbox("Beautify Lua", .{ .v = &settings.beautify_lua })) {
                try writeSettings(settings);
            }

            if (zgui.button("Convert", .{ .w = 200.0 })) {
                std.debug.print("Converting...\n", .{});

                var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
                defer arena.deinit();
                const allocator = arena.allocator();

                var diagnostics: converter.Diagnostics = .{};
                if (converter.convert(
                    settings.input_folder_path,
                    settings.output_folder_path,
                    allocator,
                    &diagnostics,
                )) {
                    if (settings.beautify_lua) {
                        try converter.beautifyLua(settings.output_folder_path, allocator);
                    }

                    // TODO: Run .convert() in a separate thread, letting it update a passed Progress struct so we can update a progress bar here?
                    // TODO: Check if std/Progress.zig is of use: https://ziglang.org/documentation/master/std/src/std/Progress.zig.html
                    // TODO: Look at this example of multithreading in Zig: https://gist.github.com/cabarger/d3879745b8477670070f826cad2f027d
                    // var progress: f32 = 0.0;
                    // zgui.pushStyleColor4f(.{ .idx = .plot_histogram, .c = .{ 0.1 + 0.5 * (1 - progress), 0.2 + 0.7 * progress, 0.3, 1.0 } });
                    // zgui.progressBar(.{ .fraction = progress, .overlay = "" });
                    // zgui.popStyleColor(.{});
                    // progress += 0.01;
                    // if (progress > 2.0) progress = 0.0;

                    std.debug.print("Done converting!\n", .{});

                    popup_slice = try std.fmt.bufPrint(&popup_buf, "The converted mods have been put in {s}", .{settings.output_folder_path});

                    zgui.openPopup("popup", .{});
                } else |err| {
                    switch (err) {
                        error.InvalidInputPath => {
                            popup_slice = try std.fmt.bufPrint(&popup_buf, "Error: Invalid input path", .{});
                        },
                        error.InvalidOutputPath => {
                            popup_slice = try std.fmt.bufPrint(&popup_buf, "Error: Invalid output path", .{});
                        },
                        error.FileNotFound => {
                            popup_slice = try std.fmt.bufPrint(&popup_buf, "Error: Please enter valid input and output paths, and make sure you didn't delete any rule files", .{});
                        },
                        error.UnexpectedToken => {
                            popup_slice = try std.fmt.bufPrint(&popup_buf, "Error: Unexpected token '{s}' in file {s} on line {} and column {}", .{
                                diagnostics.token orelse "null",
                                diagnostics.file_path orelse "null",
                                diagnostics.line orelse -1,
                                diagnostics.column orelse -1,
                            });
                        },
                        error.UnclosedMultiComment => {
                            popup_slice = try std.fmt.bufPrint(&popup_buf, "Error: Unclosed multi-line comment in file {s}", .{
                                diagnostics.file_path orelse "null",
                            });
                        },
                        error.TooManyTabs => {
                            popup_slice = try std.fmt.bufPrint(&popup_buf, "Error: Too many tabs in file {s} on line {} and column {}", .{
                                diagnostics.file_path orelse "null",
                                diagnostics.line orelse -1,
                                diagnostics.column orelse -1,
                            });
                        },
                        error.ExpectedADataModule => {
                            popup_slice = try std.fmt.bufPrint(&popup_buf, "Error: Expected a DataModule", .{});
                        },
                        error.ContainsMoreThanOneDataModule => {
                            popup_slice = try std.fmt.bufPrint(&popup_buf, "Error: The mod contains more than one DataModule", .{});
                        },
                        else => |_| {
                            popup_slice = try std.fmt.bufPrint(&popup_buf, "{?}", .{@errorReturnTrace()});
                        },
                    }

                    std.debug.print("{s}\n", .{popup_slice});
                    zgui.openPopup("popup", .{});
                }
            }

            zgui.setNextItemWidth(@max(zgui.calcTextSize(settings.game_executable_path, .{})[0] + padding, min_width));
            if (zgui.inputTextWithHint("Game executable path", .{ .hint = "Copy-paste a path from File Explorer here", .buf = &game_executable_path_mut })) {
                settings.game_executable_path = std.mem.span(@as([*:0]u8, &game_executable_path_mut));
                try writeSettings(settings);
            }

            if (zgui.button("Launch", .{ .w = 200.0 })) {
                const dirname = std.fs.path.dirname(settings.game_executable_path) orelse ".";

                if (std.posix.chdir(dirname)) {
                    var argv = [_][]const u8{settings.game_executable_path};
                    _ = try std.ChildProcess.run(.{ .argv = &argv, .allocator = gpa });
                } else |err| switch (err) {
                    error.BadPathName, error.FileNotFound => {
                        popup_slice = try std.fmt.bufPrint(&popup_buf, "Error: Please enter the game executable path", .{});
                        zgui.openPopup("popup", .{});
                    },
                    else => |e| return e,
                }
            }

            // TODO: Add the ability to zip the result back
            // if (zgui.button("Zip", .{ .w = 200.0 })) {
            //     var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
            //     defer arena.deinit();
            //     var allocator = arena.allocator();

            //     try zip(settings.input_folder_path, settings.output_folder_path, allocator);
            //     std.debug.print("Done zipping!\n", .{});
            // }

            if (zgui.beginPopup("popup", .{})) {
                zgui.text("{s}\n", .{popup_slice});
                zgui.endPopup();
            }
        }
        zgui.end();

        const swapchain_texv = gctx.swapchain.getCurrentTextureView();
        defer swapchain_texv.release();

        const commands = commands: {
            const encoder = gctx.device.createCommandEncoder(null);
            defer encoder.release();

            // GUI pass
            {
                const pass = zgpu.beginRenderPassSimple(encoder, .load, swapchain_texv, null, null, null);
                defer zgpu.endReleasePass(pass);
                zgui.backend.draw(pass);
            }

            break :commands encoder.finish(null);
        };
        defer commands.release();

        gctx.submit(&.{commands});
        _ = gctx.present();
    }
}

fn writeSettings(settings: Settings) !void {
    const output_file = try std.fs.cwd().createFile("settings.json", .{});
    defer output_file.close();

    var buffered = std.io.bufferedWriter(output_file.writer());
    const buffered_writer = buffered.writer();
    try std.json.stringify(settings, .{}, buffered_writer);
    try buffered.flush();
}
